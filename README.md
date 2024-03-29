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
![advanced_portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/41ad8978-babe-4406-8d4d-2d455358adfc)
The "Advanced Buy and Hold" strategy further reduces risk.

## Dynamic Portfolio Strategy

1. We assume that periodic reassessment and selection of the investment portfolio are necessary.
2. We assume that a business cycle is completed approximately every 5 years. Therefore, starting from the initial year of backtesting, we will recalculate the growth trends for each stock every 5 years and adjust the investment portfolio accordingly.
3. We assume that assets will be evenly allocated among the targets within the investment portfolio.
4. The selected investment portfolio:
   ### 2012 : 2330, 2340, 6271, 8271
   ### 2017 : 2303, 2330, 2329, 2458, 2344, 3583, 8150, 2449, 2379, 2351, 3413, 3006, 6257
   ### 2022 : 2303, 4952, 8081, 2330, 5471, 2436, 2458, 6239, 5285, 3592, 3443, 2344, 3583, 8150, 8016, 4967, 3034, 3532, 2449, 4961, 3016, 2302, 2379, 3545, 5222, 6202, 3014, 2351, 2388, 2441, 3413, 3006, 4968, 3661, 8261, 2408, 2337, 5269, 2338
![portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/f6775846-bb62-4acb-90c8-4f6a55c16514)

## Utilize the non-dominated sorting method

In this study, simple regression is employed to predict trends in the financial data of individual stocks. A higher slope of the simple regression line indicates a greater expected magnitude of financial performance growth for the company. On the other hand, Mean Absolute Error (MAE) is utilized as the loss function to assess the accuracy of trend predictions, with a larger MAE indicating a less accurate prediction.

Therefore, under the assumption of the effectiveness of the simple regression method, it is a reasonable choice to pursue the maximization of the slope of the simple regression line and the minimization of MAE, that is the position of the orange points in the diagram below.

If the trend line slope of a particular stock is greater than that of other assets and its MAE is smaller than others, we can say that it "Dominates" the other assets, indicating that its performance is absolutely better than the others. And when several stocks each have their own victories in terms of slope and MAE, this study considers that these stocks should be regarded as equally good. In other words, the orange points simultaneously dominate the blue points and the red points, while the orange points do not dominate each other.

In this study, we select points on the red curve (also known as the Pareto frontier) to mitigate the potential issue of having an excessive number of stocks in the investment portfolio.

![圖片2](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/3fced950-11a1-4ea2-ad91-cda637f2bced)

### Selected investment portfolio:
2012 : 2330, 6271, 8271  
2017 : 2330, 2344, 3583, 2379, 2351  
2022 : 2330, 3443, 3583, 5222, 3014, 2388, 2337, 5269  

![portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/d6c8ea16-ce6e-4997-bbcc-998f78c34388)


# Verification of significance
## Description
The research above is based on a linear regression analysis using fundamental data. However, there is one issue that needs to be addressed: after conducting the linear regression analysis, we need to confirm its significance to determine if the trend observed is statistically meaningful.    

However, when analyzing the significance of revenue, gross profit margin, and net profit margin simultaneously in selecting stocks based on the above research, the following issues may arise: The gross profit margin and net profit margin may not necessarily exhibit a clear "linear relationship" as observed in revenue.   

Currently, this study has not reached a conclusion regarding the weighting of these three indicators. Simultaneously considering the results of linear regression analyses of these three types of data may pose challenges during the stock selection phase.   

Therefore, this study decides to base its selection on the linear regression results of revenue rate, picking stocks that are statistically "significant" and exhibit a "high degree of correlation."  

However, the linear regression results of gross profit margin and net profit margin will be used as auxiliary tools for manual assessment, temporarily excluded from the formalized stock selection method.  

Therefore, the stock selection criteria based on the experimental results will rely on linear regression analysis of revenue and time, with the following conditions:  
Significance (p-value < 0.05)  
High correlation (slope > 0.5)  

And each time stocks are selected under the condition of "significance," the top five stocks with the highest correlation will be chosen.  
If no stocks meet the criteria for selection during that particular round, then 0050 (the market index) will be purchased. 

## Result
![portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/eb13607b-08e9-4792-a1d8-59e3037c3b16)

## Selected investment portfolio
### ALL
2012 : 2330, 2351, 2451, 2454, 2481, 6271  
2017 : 2330, 2454, 3034, 6271  
2022 : 2330, 2379, 2408, 2454, 3016, 3034, 3443, 3530, 3661, 4961, 4968, 5222, 6257, 8016  

### TOP5
2012 : 2481, 2330, 2454, 2451, 6271  
2017 : 2330, 2454, 6271, 3034  
2022 : 2330, 2454, 3530, 3034, 4961  


# Add consideration for slippage
## Description
Due to the restricted trading hours of the Taiwan stock market from 9:00 AM to 1:30 PM on weekdays, price gaps may occur at the market open, causing stocks to open higher or lower than their previous closing prices. This practical challenge makes it difficult to precisely match the "stop-loss" price with the values set in the experimental setup. To address this issue, this study incorporates consideration for slippage, setting the cost of each "entry and exit" at 3%.

## Result
![portfolio](https://github.com/bffdhw/tw_stock_analysis/assets/34659552/31f7cf5d-589a-40d5-8471-8e0b93a344d4)


# Conclusion
In targets with a long-term upward trend in stock prices, using the Advanced Buy and Hold strategy appears to help mitigate the volatility risk associated with the original Buy and Hold strategy, especially in situations where there is a minimal impact on the return rate.

Financial statement analysis, capable of selecting targets with a high probability of long-term growth, aligns well with the scenario for employing the Advanced Buy and Hold strategy. Even in the selection of stocks with a long-term decline, losses can be reduced through the use of a stop-loss mechanism.

# Potential Risks and Areas for Improvement
1. Currently, the strategy is only being tested in the semiconductor industry. In the future, it will be necessary to apply it to various other industries to validate the robustness of the strategy.

# Other considerations to note
1. Taiwanese regulations mandate that companies must disclose their annual financial report for the previous year by March 31 of the following year. However, this research's backtesting period starts on January 1. Therefore, the backtesting period for this study will be from 04/01 to 03/31.

