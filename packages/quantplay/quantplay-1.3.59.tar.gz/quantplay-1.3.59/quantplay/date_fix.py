from quantplay.service import market

interval = "15minute"
path = market.nse_opt_path
symbols = ['NIFTY2260217300PE', 'NIFTY2250516600CE', 'NIFTY2242118300PE'
    , 'NIFTY2242115900PE', 'NIFTY2242118150PE', 'NIFTY2240717800CE'
    , 'NIFTY2242116550CE', 'NIFTY2242116450PE', 'NIFTY2242118100PE'
    , 'NIFTY2260216650CE', 'NIFTY2242116500PE', 'NIFTY2240717900PE'
    , 'NIFTY2260215650PE', 'NIFTY2242116700PE', 'NIFTY2260916800CE'
    , 'NIFTY2251916400PE', 'NIFTY2242115950PE', 'NIFTY2242118250PE'
    , 'NIFTY2242117750PE', 'NIFTY2260916350CE', 'NIFTY2242116950PE'
    , 'NIFTY2260916200CE', 'NIFTY2260217050PE', 'NIFTY2240716800PE'
    , 'NIFTY2260216950CE', 'NIFTY2242116000CE', 'NIFTY2251216150PE'
    , 'NIFTY2242116850PE', 'NIFTY2260216950PE', 'NIFTY2260916250PE'
    , 'NIFTY22APR16150PE', 'NIFTY2260917700PE', 'NIFTY2242116200CE'
    , 'NIFTY2260216650PE', 'NIFTY2242116150CE', 'NIFTY2260216450PE'
    , 'NIFTY2250516050PE', 'NIFTY2260916950CE', 'NIFTY2242116550PE'
    , 'NIFTY2260215700CE', 'NIFTY2251916350PE', 'NIFTY2260217350CE'
    , 'NIFTY2240716550PE', 'NIFTY2242117050PE', 'NIFTY2242117800PE'
    , 'NIFTY2260217350PE', 'NIFTY2260217550PE', 'NIFTY2242115900CE'
    , 'NIFTY2260216200CE', 'NIFTY2242116200PE', 'NIFTY2242116300PE'
    , 'NIFTY2242116100CE', 'NIFTY2242116250CE', 'NIFTY2242116500CE'
    , 'NIFTY2250515950CE', 'NIFTY2242117700PE', 'NIFTY2251216250PE'
    , 'NIFTY2242116400CE', 'NIFTY2250516900CE', 'NIFTY2250516250CE'
    , 'NIFTY2242117150PE', 'NIFTY2242116400PE', 'NIFTY2251216350PE'
    , 'NIFTY2242118350CE', 'NIFTY2242116050CE', 'NIFTY2251916100PE'
    , 'NIFTY2260217150PE', 'NIFTY2242117850CE', 'NIFTY2260216550PE'
    , 'NIFTY2260917750PE', 'NIFTY2242116050PE', 'NIFTY2242117900CE'
    , 'NIFTY2242117950PE', 'NIFTY2240718200CE', 'NIFTY2260917250CE'
    , 'NIFTY2260216900CE', 'NIFTY2250515700PE', 'NIFTY2260216850PE'
    , 'NIFTY2250515600PE', 'NIFTY2260215850CE', 'NIFTY2260916850CE'
    , 'NIFTY2250515900PE', 'NIFTY22MAY16350PE', 'NIFTY2242118000PE'
    , 'NIFTY2260217650PE', 'NIFTY2251916800PE', 'NIFTY2242116300CE'
    , 'NIFTY2250515800PE', 'NIFTY2260217650CE', 'NIFTY2242116600PE'
    , 'NIFTY2260917550PE', 'NIFTY2242116800PE', 'NIFTY2241317900CE'
    , 'NIFTY2251916200PE', 'NIFTY2260216700CE', 'NIFTY2250516600PE'
    , 'NIFTY2240716500PE', 'NIFTY2242115950CE', 'NIFTY2260216300PE'
    , 'NIFTY2260917750CE', 'NIFTY2242117800CE', 'NIFTY2260916750CE'
    , 'NIFTY2242118300CE', 'NIFTY2242116350PE', 'NIFTY2260217100CE'
    , 'NIFTY2242117000PE', 'NIFTY2242118350PE', 'NIFTY2242116150PE'
    , 'NIFTY2260216450CE', 'NIFTY2240718000PE', 'NIFTY2242117650PE'
    , 'NIFTY2260217250PE', 'NIFTY2242116650PE', 'NIFTY2240717100PE'
    , 'NIFTY2260216600CE', 'NIFTY2242118200PE', 'NIFTY2242117700CE'
    , 'NIFTY2250516800CE', 'NIFTY2242115800CE', 'NIFTY2242116750PE'
    , 'NIFTY2242116100PE', 'NIFTY2242116350CE', 'NIFTY2250516000PE'
    , 'NIFTY2260916350PE', 'NIFTY2260917350CE', 'NIFTY2250516150PE'
    , 'NIFTY2242115850CE', 'NIFTY2242116450CE', 'NIFTY2260917650CE'
    , 'NIFTY2242117600PE', 'NIFTY2250516700CE', 'NIFTY2242117250CE'
    , 'NIFTY2260217550CE', 'NIFTY2242116000PE', 'NIFTY2260916850PE'
    , 'NIFTY2251216100PE', 'NIFTY2242116900PE']
for symbol in symbols:
    print(symbol)
    data = market.data_by_path(interval=interval, symbols=[symbol], path=market.nse_opt_path)

    data.loc[:, 'date'] = data.date.astype(str).apply(lambda x: x.split("+")[0])
    data.to_csv(f"{path}/{interval}/{symbol}.csv", index=False)
