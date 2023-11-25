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

## Data
For the sake of having a consistent baseline across different stocks, this study standardizes the data starting from the year 2002 (excluding stocks that do not meet the criteria). Trend predictions are conducted for the period from 2002 to 2011, spanning a total of 10 years. Subsequently, a buy-and-hold strategy is backtested from 2012 to 2023/11.
![flowchart](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/97289e11-16cb-49c7-a89c-c0a03aa34415)

## Define "Trend"
The research assumes that if financial data demonstrates a positive growth trend, the stock price may also experience an upward trend. Therefore, defining financial indicators as showing positive growth becomes crucial. In this study, financial data spanning 10 years from 2002 to 2011, including but not limited to revenue, net profit, gross profit, etc., is utilized. Linear regression is employed as a reference standard for trend analysis. If the slope of the regression line is positive, it is considered indicative of an upward growth trend for the respective indicator.

![revenue(%)_Indicator](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/daa69382-10cd-4c54-9290-e23e8eb8683c)
![net_income(%)_Indicator](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/36921dda-860d-4f85-bc1a-fff920879b57)
![gross_profit(%)_Indicator](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/a019066a-1717-4563-82da-40f7f3247c79)



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
Screening Criteria : (net_income(%)_coef > 0) & (gross_profit(%)_coef > 0)
![2302](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/963bfd51-025b-4bfc-8fa6-baf30c5be746)
![2329](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/97774f6a-e2ac-406d-955f-8cfb6cbfadfc)
![2330](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/eed6bf13-05b3-482f-8562-605fda7619ac)
![2340](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/2d38d650-9ef8-4f4d-ace6-683fd66621b9)
![6202](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/9cf125b2-e56f-4824-bea2-419ad67106d3)
![8271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/04e15028-1bd6-48b2-91d7-f1ca49813209)
![6271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/e05767d6-689f-4d5a-8193-efc1b1f3911f)
![3041](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/8e5a0b75-c39a-4c9c-bf34-2b4e0869870c)

### portfolio
![portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/5ead418d-b5ee-4ed0-934f-9d36fd59530a)
The results indicate that even though the selected stocks include those with higher volatility and long-term declines, the portfolio's performance still outperforms the overall market (currently comprised only of semiconductor industry stocks).



## Advanced Buy And Hold Strategy
The core idea of this strategy is based on a buy-and-hold approach, but with the aim of avoiding the risk of drawdowns. The method employed involves selling the accumulated position when the cumulative profit and loss falls by a certain percentage. After the price recovers, the position is bought back. It's worth noting that this method may incur higher frictional costs, especially during market fluctuations or oscillations.
![6271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/481a3f8a-df8a-4176-be49-8d02d7d71e33)
![6202](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/35d488f4-fb8b-4d1c-b2ed-74244146a447)
![2340](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/f2533bf5-a397-473a-8f9d-00f47d8a0c1a)
![2330](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/a6568f25-2cb1-409a-aa34-d421dab87daf)
![2329](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/afcd9cbd-f26e-47c4-9701-91f3d34b85a8)
![2302](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/12e84877-83ae-461b-9f51-6edf1a7c0665)
![8271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/273ca709-6e2c-4ad6-abc2-3904c333cf1f)
The results indicate that this approach can reduce the volatility risk of a buy-and-hold strategy(excluding considerations for slippage, transaction fees, and taxes).

Even when filtering stocks with a long-term downward trend, losses can be mitigated by incorporating stop-loss measures to avoid further purchases. 
![3041](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/24043e03-a6e1-4991-842f-5b128627d91b)

## Advanced Buy And Hold Strategy Portfolio
![advanced_portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/333ded73-0866-43bc-926c-bc454167787c)


## Using Increased Revenue as a Filtering Criterion
Screening Criteria : (net_income(%)_coef > 0) & (gross_profit(%)_coef > 0) & (revenue(%)_coef > 0)
![8271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/32018c75-644c-45d1-b84a-5dd27659292d)
![6271](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/766ec7c5-cf2c-4d0b-8be3-f380554402b8)
![2340](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/fcf20610-99b9-4fbe-9ebc-d607b47bd8b4)
![2330](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/692af939-99bc-41ea-b755-fa25cc263980)
Adding revenue as a criterion for selecting good stocks can help filter out targets (such as 3041) with a long-term decline in stock prices.

Original Buy and Hold Portfolio
![original_portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/b1245c96-cdf3-48b1-94f9-e4944240684b)

Advanced Buy and Hold Portfolio
![advanced_portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/fec1bd6c-c97e-4502-89de-8e92eb9e9056)
The "Advanced Buy and Hold" strategy further reduces risk.

# Conclusion
In targets with a long-term upward trend in stock prices, using the Advanced Buy and Hold strategy appears to help mitigate the volatility risk associated with the original Buy and Hold strategy, especially in situations where there is a minimal impact on the return rate.

Financial statement analysis, capable of selecting targets with a high probability of long-term growth, aligns well with the scenario for employing the Advanced Buy and Hold strategy. Even in the selection of stocks with a long-term decline, losses can be reduced through the use of a stop-loss mechanism.

# Potential Risks and Areas for Improvement

1. The current strategy involves backtesting with data from the previous 10 years leading up to 2012. Further validation is still needed to determine if the stock selection method is applicable for each period in a sliding window.
2. Currently, the strategy is only being tested in the semiconductor industry. In the future, it will be necessary to apply it to various other industries to validate the robustness of the strategy.
3. Taiwanese regulations mandate that companies must disclose their annual financial report for the previous year by March 31 of the following year. However, this research's backtesting period starts on January 1. In other words, there may be a potential error due to delayed financial report disclosures, leading to an overestimation of the backtested profit and loss.
4. In the current experiment, factors such as slippage, taxes, and transaction fees have not been taken into account. Therefore, the actual profit and loss may be further adjusted downward.

