"""
This trading strategy involves basic mean reversion (Bollinger Bands)

We will be trading only SPY, the S&P500 stock market index.

Strategy
When the price of SPY drops below its 21-day moving average - 1.5 * the standard deviation,
we long 100% on SPY. When price of SPY increases above its 21-day moving average + 1.5 * 
the standard deviation, we short 100% on SPY. The logic behind this is that we expect short-term 
reversal on the price action. We close our position when SPY price reaches abck to its 21-day MA.

Backtesting Results
Start Date: 12-6-2021
End Date: 24-12-2022
Sharpe: 0.367
Max Drawdown: 9.8%
Alpha: 0.053
Beta: 0.217
Win rate: 64%


""" 

# region imports
from AlgorithmImports import *
# endregion

class CrawlingOrangeDinosaur(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 6, 12)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.spy = self.AddEquity('SPY', Resolution.Daily).Symbol
        self.SetWarmUp(21)

        self.SetBenchmark("SPY")

    def OnData(self, data: Slice):
 

        hist = self.History(self.spy, timedelta(21), Resolution.Daily)['close']
        mov_avg = hist.mean()
        std_dev = 1.5 * hist.std()
        price  = self.Securities[self.spy].Price


        if not self.Portfolio.Invested:
            if price < mov_avg - std_dev:
                self.SetHoldings(self.spy, 1)

            elif price > mov_avg + std_dev:
                self.SetHoldings(self.spy, -1)


        if self.Portfolio[self.spy].IsLong:
            if price >= mov_avg:
                self.Liquidate()
        elif self.Portfolio[self.spy].IsShort:
            if price <= mov_avg:
                self.Liquidate()