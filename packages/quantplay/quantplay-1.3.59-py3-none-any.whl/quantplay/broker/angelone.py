import json
import time
import traceback

import pandas as pd
import pyotp
from retrying import retry
from SmartApi import SmartConnect

from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import InvalidArgumentException
from quantplay.utils.exchange import Market as MarketConstants
from quantplay.exception.exceptions import (
    QuantplayOrderPlacementException,
    TokenException,
    ServiceException,
)
import requests, pickle, codecs
import _thread as thread
from quantplay.utils.pickle_utils import PickleUtils
import numpy as np

from quantplay.utils.constant import Constants, OrderType


class AngelOne(Broker):

    order_sl = "STOPLOSS_LIMIT"
    order_slm = "STOPLOSS_MARKET"

    def __init__(
        self,
        order_updates=None,
        api_key=None,
        user_id=None,
        mpin=None,
        totp=None,
        wrapper=None,
    ):
        super(AngelOne, self).__init__()
        self.order_updates = order_updates

        try:
            if wrapper:
                self.set_wrapper(wrapper)
            else:
                self.wrapper = SmartConnect(api_key=api_key)
                self.wrapper.generateSession(user_id, mpin, pyotp.TOTP(totp).now())
        except Exception as e:
            raise TokenException(str(e))

        token_data = self.wrapper.generateToken(self.wrapper.refresh_token)

        self.refresh_token = token_data["data"]["refreshToken"]
        self.jwt_token = token_data["data"]["jwtToken"]
        self.user_id = self.wrapper.userId
        self.api_key = self.wrapper.api_key

        self.load_instrument()

    def set_wrapper(self, serialized_wrapper):
        self.wrapper = pickle.loads(
            codecs.decode(serialized_wrapper.encode(), "base64")
        )

    def load_instrument(self):
        try:
            self.symbol_data = PickleUtils.load_data("angelone_instruments")
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception as e:
            symbol_data = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
            data = requests.get(symbol_data)
            inst_data = json.loads(data.content)
            inst_data = pd.DataFrame(inst_data)
            self.instrument_data = inst_data[
                (inst_data.exch_seg.isin(["NFO", "MCX", "CDS"]))
                | (
                    (inst_data.exch_seg == "NSE")
                    & (inst_data.symbol.str.contains("-EQ"))
                )
            ]

            self.instrument_data.loc[:, "instrument_symbol"] = self.instrument_data.name
            self.instrument_data.loc[
                :, "instrument_expiry"
            ] = self.instrument_data.expiry
            self.instrument_data.loc[
                :, "instrument"
            ] = self.instrument_data.instrumenttype
            self.instrument_data.loc[:, "strike_price"] = (
                self.instrument_data.strike.astype(float) / 100
            )
            self.instrument_data.loc[:, "exchange"] = self.instrument_data.exch_seg
            self.instrument_data.loc[:, "option_type"] = np.where(
                "PE" == self.instrument_data.symbol.str[-2:], "PE", "CE"
            )
            self.instrument_data.loc[:, "option_type"] = np.where(
                self.instrument_data.instrument.str.contains("OPT"),
                self.instrument_data.option_type,
                None,
            )

            self.initialize_expiry_fields()
            self.add_quantplay_fut_tradingsymbol()
            self.add_quantplay_opt_tradingsymbol()

            self.instrument_data = self.instrument_data[
                [
                    "token",
                    "symbol",
                    "strike_price",
                    "exchange",
                    "option_type",
                    "instrument",
                    "tradingsymbol",
                    "expiry",
                ]
            ]
            self.instrument_data.loc[:, "broker_symbol"] = self.instrument_data.symbol

            self.initialize_symbol_data(save_as="angelone_instruments")

        self.initialize_broker_symbol_map()

    def get_symbol(self, symbol):
        if symbol not in self.quantplay_symbol_map:
            return symbol
        return self.quantplay_symbol_map[symbol]

    def get_order_type(self, order_type):
        if order_type == OrderType.sl:
            return AngelOne.order_sl
        elif order_type == OrderType.slm:
            return AngelOne.order_slm

        return order_type

    def get_product(self, product):
        if product == "NRML":
            return "CARRYFORWARD"
        elif product == "CNC":
            return "DELIVERY"
        elif product == "MIS":
            return "INTRADAY"
        elif product in ["BO", "MARGIN", "INTRADAY", "CARRYFORWARD", "DELIVERY"]:
            return product

        raise InvalidArgumentException(
            "Product {} not supported for trading".format(product)
        )

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def get_ltp(self, exchange=None, tradingsymbol=None):
        if tradingsymbol in MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP:
            tradingsymbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[
                tradingsymbol
            ]

        symbol_data = self.symbol_data[f"{exchange}:{self.get_symbol(tradingsymbol)}"]
        symboltoken = symbol_data["token"]

        if exchange == "NSE" and tradingsymbol not in ["NIFTY", "BANKNIFTY"]:
            tradingsymbol = "{}-EQ".format(tradingsymbol)

        response = self.wrapper.ltpData(exchange, tradingsymbol, symboltoken)
        if "status" in response and response["status"] == False:
            raise InvalidArgumentException(
                "Failed to fetch ltp broker error {}".format(response)
            )

        return response["data"]["ltp"]

    def place_order(
        self,
        tradingsymbol=None,
        exchange=None,
        quantity=None,
        order_type=None,
        transaction_type=None,
        tag=None,
        product=None,
        price=None,
        trigger_price=None,
    ):
        try:
            if trigger_price == 0:
                trigger_price = None

            order_type = self.get_order_type(order_type)
            product = self.get_product(product)
            tradingsymbol = self.get_symbol(tradingsymbol)
            variety = "NORMAL"
            if order_type in [AngelOne.order_sl, AngelOne.order_slm]:
                variety = "STOPLOSS"

            symbol_data = self.symbol_data[
                f"{exchange}:{self.get_symbol(tradingsymbol)}"
            ]
            symbol_token = symbol_data["token"]

            order = {
                "transactiontype": transaction_type,
                "variety": variety,
                "tradingsymbol": tradingsymbol,
                "ordertype": order_type,
                "triggerprice": trigger_price,
                "exchange": exchange,
                "symboltoken": symbol_token,
                "producttype": product,
                "price": price,
                "quantity": quantity,
                "duration": "DAY",
                "ordertag": tag,
            }

            Constants.logger.info("[PLACING_ORDER] {}".format(json.dumps(order)))
            return self.wrapper.placeOrder(order)
        except Exception as e:
            print(traceback.print_exc())
            raise QuantplayOrderPlacementException(str(e))

    def get_variety(self, variety):
        if variety == "regular":
            return "NORMAL"
        return variety

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def modify_order(self, data):
        try:
            orders = self.orders()
            order = orders[orders.order_id == str(data["order_id"])].to_dict("records")[
                0
            ]
            quantity = order["quantity"]
            token = order["token"]
            exchange = order["exchange"]
            product = self.get_product(order["product"])
            variety = order["variety"]
            order_type = self.get_order_type(data["order_type"])
            if "trigger_price" not in data:
                data["trigger_price"] = None
            if "quantity" in data and int(data["quantity"]) > 0:
                quantity = data["quantity"]
            order_id = data["order_id"]

            order_params = {
                "orderid": order_id,
                "variety": variety,
                "price": data["price"],
                "trigger_price": data["trigger_price"],
                "producttype": product,
                "duration": "DAY",
                "quantity": quantity,
                "symboltoken": token,
                "ordertype": order_type,
                "exchange": exchange,
                "tradingsymbol": self.get_symbol(order["tradingsymbol"]),
            }

            Constants.logger.info(
                f"Modifying order [{order_id}] params [{order_params}]"
            )
            response = self.wrapper.modifyOrder(order_params)
            Constants.logger.info(f"[MODIFY_ORDER_RESPONSE] {response}")
            return response
        except Exception as e:
            print(traceback.print_exc())
            Constants.logger.error(
                f"[ORDER_MODIFY_FAILED] for {data['order_id']} failed with exception {e}"
            )

    def cancel_order(self, order_id, variety="NORMAL"):
        self.wrapper.cancelOrder(order_id=order_id, variety=variety)

    def positions(self):
        positions = self.wrapper.position()

        if positions["data"] is None:
            return pd.DataFrame(columns=self.positions_column_list)

        positions = pd.DataFrame(positions["data"])

        if "optiontype" not in positions.columns:
            positions.loc[:, "optiontype"] = None

        positions.rename(
            columns={
                "optiontype": "option_type",
                "sellqty": "sell_quantity",
                "buyqty": "buy_quantity",
                "producttype": "product",
                "symboltoken": "token",
            },
            inplace=True,
        )

        positions.loc[:, "buy_quantity"] = positions.buy_quantity.astype(int)
        positions.loc[:, "sell_quantity"] = positions.sell_quantity.astype(int)
        positions.loc[:, "quantity"] = positions.buy_quantity - positions.sell_quantity

        positions["product"] = positions["product"].replace(
            ["DELIVERY", "CARRYFORWARD", "INTRADAY"], ["CNC", "NRML", "MIS"]
        )

        return positions[self.positions_column_list]

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def orders(self, tag=None, status=None):
        order_book = self.wrapper.orderBook()
        if order_book["data"]:
            orders = pd.DataFrame(order_book["data"])

            positions = self.positions()
            if len(orders) == 0:
                return pd.DataFrame(columns=self.orders_column_list)

            positions = (
                positions.sort_values("product").groupby(["tradingsymbol"]).head(1)
            )
            orders = pd.merge(
                orders,
                positions[["tradingsymbol", "ltp"]],
                how="left",
                left_on=["tradingsymbol"],
                right_on=["tradingsymbol"],
            )

            orders.loc[:, "update_timestamp"] = pd.to_datetime(orders.updatetime)
            orders.rename(
                columns={
                    "orderid": "order_id",
                    "uid": self.user_id,
                    "ordertag": "tag",
                    "averageprice": "average_price",
                    "producttype": "product",
                    "transactiontype": "transaction_type",
                    "triggerprice": "trigger_price",
                    "price": "price",
                    "filledshares": "filled_quantity",
                    "unfilledshares": "pending_quantity",
                    "updatetime": "order_timestamp",
                    "info": "text",
                    "ordertype": "order_type",
                    "symboltoken": "token",
                },
                inplace=True,
            )

            existing_columns = list(orders.columns)
            columns_to_keep = list(
                set(self.orders_column_list).intersection(set(existing_columns))
            )
            orders = orders[columns_to_keep]

            orders.loc[:, "order_timestamp"] = pd.to_datetime(orders.order_timestamp)
            orders = self.filter_orders(orders, status=status, tag=tag)

            orders.status = orders.status.replace(
                ["open", "cancelled", "trigger pending", "complete"],
                ["OPEN", "CANCELLED", "TRIGGER PENDING", "COMPLETE"],
            )
            orders["product"] = orders["product"].replace(
                ["DELIVERY", "CARRYFORWARD", "INTRADAY"], ["CNC", "NRML", "MIS"]
            )
            orders["order_type"] = orders["order_type"].replace(
                [AngelOne.order_sl, AngelOne.order_slm], [OrderType.sl, OrderType.slm]
            )
            return orders
        else:
            if "message" in order_book and order_book["message"] == "SUCCESS":
                return pd.DataFrame(columns=self.orders_column_list)
            if "errorcode" in order_book and order_book["errorcode"] == "AB1010":
                raise TokenException(
                    "Can't Fetch order book because session got expired"
                )
            else:
                print(order_book)
                print(traceback.print_exc())
                raise ServiceException("Unknown error while fetching order book [{}]")

    def profile(self):
        profile_data = self.wrapper.getProfile(self.refresh_token)["data"]
        response = {
            "user_id": profile_data["clientcode"],
            "full_name": profile_data["name"],
            "email": profile_data["email"],
        }

        return response

    def account_summary(self):
        margins = self.wrapper.rmsLimit()["data"]

        pnl = 0
        # positions = self.positions()
        # if len(positions) > 0:
        #     pnl = positions.pnl.sum()

        response = {
            "margin_used": margins["net"],
            "total_balance": margins["net"],
            "margin_available": margins["net"],
            "pnl": pnl,
        }
        return response
