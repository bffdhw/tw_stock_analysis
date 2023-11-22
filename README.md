# tw_stock_analysis

This is a leisure-time programming exercise. It may contain many bugs. I will update it when I have time to make it more refined.

# Abstract
This is a study based on the Taiwan stock market, aiming to identify excellent companies for investment through the analysis of individual stock financial data. The goal is to outperform the overall market performance.

# Research Motivation

1. To select individual stocks with growth potential and form a portfolio to outperform the overall market.
2. Limited success has been achieved in technical analysis based on price and volume relationships (in my personal experience).
3. To gain greater confidence in long-term stock holding through fundamental analysis based on financial data.

# Research Objectives

1. Good Stock Selection Strategy: Utilize financial data of various companies as criteria for stock screening.
2. Active Buy and Hold Trading Strategy: Attempt to optimize the buy and hold strategy with the goal of increasing returns and reducing risk.

# Research Methods

## Stock Selection Strategy

1. This study assumes that annual financial report data is sufficient to reflect a company's past and, to some extent, future operational performance.
2. The use of annual data results in a smaller dataset (less than 100 data per company). Linear regression is initially chosen as the model for predicting future trends.
3. Key financial indicators considered include revenue ratio, gross profit margin, net profit margin, as well as debt repayment capability, dividend data, and others.
4. Stocks exhibiting a positive trend in financial indicators are selected.

## Trading Strategy

1. After selecting stocks, backtest the performance using a buy and hold strategy, and compare it with the market benchmark.
2. The market benchmark is set as the Taiwan stock market's 0050 index.
3. Attempt to enhance profit-taking and stop-loss strategies based on the core of buy and hold, and compare the results with the market benchmark.

# Experimental Results 

# Basic Buy And Hold Strategy
## good
![2302](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/963bfd51-025b-4bfc-8fa6-baf30c5be746)
![2329](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/97774f6a-e2ac-406d-955f-8cfb6cbfadfc)
![2330](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/eed6bf13-05b3-482f-8562-605fda7619ac)
![2340](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/2d38d650-9ef8-4f4d-ace6-683fd66621b9)
![6202](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/9cf125b2-e56f-4824-bea2-419ad67106d3)

## high risk
![8271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/04e15028-1bd6-48b2-91d7-f1ca49813209)
![6271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/e05767d6-689f-4d5a-8193-efc1b1f3911f)

## trash
![3041](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/8e5a0b75-c39a-4c9c-bf34-2b4e0869870c)


# Active Buy And Hold Strategy(stop loss)
![8271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/2653c5f1-e3c7-4e49-b3ef-b7ec269207a7)
![6271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/1f56ecf9-05ad-43ca-bcce-ce66ad8fd746)
![6202](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/4afd6fd8-91f7-4722-84d6-bca55b8e51dc)
![3041](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/2cdbfcba-51cd-4d61-b5f8-b678e307b21a)
![2340](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/c0707c6d-9ab3-45ec-97f7-04f88db642df)
![2330](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/d246dbc5-1bfa-43d6-b2ef-0d222926513b)
![2329](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/84a496f7-1a1c-4299-9314-7daefaf9379b)
![2302](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/635241a4-3dae-45f8-8ae7-5dbcccd098f9)









