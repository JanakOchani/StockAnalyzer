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
        print(" Do it here ")
        self.growth_pct_change = 0.0

    def setVerdictAndReason(self):
        print("Evaluate Verdict And Reason")
        self.vedict=""
        self.reason=""


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
            "PREVIOUS CASH": self.previous_cash
        }



