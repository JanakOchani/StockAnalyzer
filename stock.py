class Stock:
    def __init__(self, l_ticker):
        self.ticker = l_ticker
        self.current_price = 0
        self.pe_ratio = 0

        self.latest_revenue = 0
        self.latest_profit = 0
        self.latest_cash = 0

        self.previous_revenue = 0
        self.previous_profit = 0
        self.previous_cash = 0

        self.growth_pct_change = None
        self.verdict = None
        self.reason = None

    def setPrice(self, l_price):
        self.current_price = l_price

    def setPERatio(self, l_pe):
        self.pe_ratio = l_pe

    def setLatestRevenue(self, val):
        self.latest_revenue = val

    def setLatestProfit(self, val):
        self.latest_profit = val

    def setLatestCash(self, val):
        self.latest_cash = val

    def setPreviousRevenue(self, val):
        self.previous_revenue = val

    def setPreviousProfit(self, val):
        self.previous_profit = val

    def setPreviousCash(self, val):
        self.previous_cash = val

    def setProfitGrowthPercentage(self):
        if self.latest_profit and self.previous_profit and self.previous_profit != 0:
            self.growth_pct_change = round(
                ((self.latest_profit - self.previous_profit) / self.previous_profit) * 100,
                2
            )

    def setVerdictAndReason(self):
        trailing_pe = self.pe_ratio
        profit_growth_pct = self.growth_pct_change

        if trailing_pe is None or profit_growth_pct is None:
            self.verdict = "Fair"
            self.reason = "Not enough data"

        elif trailing_pe < 22 and profit_growth_pct > 12:
            self.verdict = "Not so expensive"
            self.reason = f"Good profit growth ({profit_growth_pct}%) with reasonable PE."

        elif trailing_pe > 35:
            self.verdict = "Looks expensive"
            self.reason = f"High PE ratio ({trailing_pe})."

        else:
            self.verdict = "Fairly valued"
            self.reason = f"PE is {trailing_pe} and profit growth is {profit_growth_pct}%."

    def getJSON(self):
        return {
            "TICKER": self.ticker,
            "CURRENT PRICE": self.current_price,
            "P/E RATIO": self.pe_ratio,
            "LATEST REVENUE": self.latest_revenue,
            "LATEST PROFIT": self.latest_profit,
            "LATEST CASH": self.latest_cash,
            "PREVIOUS REVENUE": self.previous_revenue,
            "PREVIOUS PROFIT": self.previous_profit,
            "PREVIOUS CASH": self.previous_cash,
            "PROFIT GROWTH %": self.growth_pct_change,
            "VERDICT": self.verdict,
            "REASON": self.reason
        }