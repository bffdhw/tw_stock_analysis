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

## Basic Buy And Hold Strategy
### good
![2302](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/963bfd51-025b-4bfc-8fa6-baf30c5be746)
![2329](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/97774f6a-e2ac-406d-955f-8cfb6cbfadfc)
![2330](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/eed6bf13-05b3-482f-8562-605fda7619ac)
![2340](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/2d38d650-9ef8-4f4d-ace6-683fd66621b9)
![6202](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/9cf125b2-e56f-4824-bea2-419ad67106d3)

### high risk
![8271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/04e15028-1bd6-48b2-91d7-f1ca49813209)
![6271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/e05767d6-689f-4d5a-8193-efc1b1f3911f)

### trash
![3041](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/8e5a0b75-c39a-4c9c-bf34-2b4e0869870c)

### portfolio
![portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/5ead418d-b5ee-4ed0-934f-9d36fd59530a)
The results indicate that even though the selected stocks include those with higher volatility and long-term declines, the portfolio's performance still outperforms the overall market (currently comprised only of semiconductor industry stocks).



## Advanced Buy And Hold Strategy
![6271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/481a3f8a-df8a-4176-be49-8d02d7d71e33)
![6202](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/35d488f4-fb8b-4d1c-b2ed-74244146a447)
![3041](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/24043e03-a6e1-4991-842f-5b128627d91b)
![2340](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/f2533bf5-a397-473a-8f9d-00f47d8a0c1a)
![2330](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/a6568f25-2cb1-409a-aa34-d421dab87daf)
![2329](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/afcd9cbd-f26e-47c4-9701-91f3d34b85a8)
![2302](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/12e84877-83ae-461b-9f51-6edf1a7c0665)
![advanced_portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/dedd5fe7-0e2f-4008-8f38-c916d5e7208d)
![8271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/273ca709-6e2c-4ad6-abc2-3904c333cf1f)


## Advanced Buy And Hold Strategy Portfolio
![advanced_portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/333ded73-0866-43bc-926c-bc454167787c)


## Using Increased Revenue as a Filtering Criterion
![8271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/32018c75-644c-45d1-b84a-5dd27659292d)
![6271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/766ec7c5-cf2c-4d0b-8be3-f380554402b8)
![2340](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/fcf20610-99b9-4fbe-9ebc-d607b47bd8b4)
![2330](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/692af939-99bc-41ea-b755-fa25cc263980)

Original Buy and Hold Portfolio
![original_portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/b1245c96-cdf3-48b1-94f9-e4944240684b)

Advanced Buy and Hold Portfolio
![advanced_portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/fec1bd6c-c97e-4502-89de-8e92eb9e9056)



