import yfinance as yf

from database import Database
from stock import Stock


class Analyze:
    def __init__(self):
        print("From analyze class: Contructor created.")

    def analyzeStock(self, ticker):
        print(f"From analyze class: This {ticker} has been called.")
        try:

            ticker = ticker.upper()
            stock = yf.Ticker(ticker)
            info = stock.info

            financials = stock.financials
            balance = stock.balance_sheet

            # Latest year
            latest_revenue = financials.loc['Total Revenue'].iloc[0] if 'Total Revenue' in financials.index else None
            latest_profit = financials.loc['Net Income'].iloc[0] if 'Net Income' in financials.index else None
            latest_cash = balance.loc['Cash And Cash Equivalents'].iloc[0] if 'Cash And Cash Equivalents' in balance.index else None

            # Previous year
            previous_revenue = financials.loc['Total Revenue'].iloc[1] if len(financials.columns) > 1 else None
            previous_profit = financials.loc['Net Income'].iloc[1] if len(financials.columns) > 1 else None
            previous_cash = balance.loc['Cash And Cash Equivalents'].iloc[1] if len(balance.columns) > 1 else None

            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            current_price = float(current_price)
            print(f"The current price of {ticker} is {current_price})")

            trailing_pe = info.get('trailingPE')
            print(f"The P/E ratio of {ticker} is {trailing_pe}")

            analyzedStock = Stock(ticker)
            analyzedStock.setPrice(current_price)
            analyzedStock.setPERatio(trailing_pe)

            analyzedStock.setLatestRevenue(latest_revenue)
            analyzedStock.setLatestProfit(latest_profit)
            analyzedStock.setLatestCash(latest_cash)

            analyzedStock.setPreviousRevenue(previous_revenue)
            analyzedStock.setPreviousProfit(previous_profit)
            analyzedStock.setPreviousCash(previous_cash)

            analyzedStock.setProfitGrowthPercentage()
            analyzedStock.setVerdictAndReason()

            self.storeStock(analyzedStock)

            print(f"The current price of {analyzedStock} is {analyzedStock.current_price}")
            return analyzedStock

        except Exception as error:
            print("Error while fetching the ticker:", error)


    def storeStock(self, analyzedStock):
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS stock_fundamentals(
            ticker_name VARCHAR(10),
            current_price FLOAT,
            pe_ratio FLOAT,
            latest_revenue BIGINT,
            latest_profit BIGINT,
            latest_cash BIGINT,
            previous_revenue BIGINT,
            previous_profit BIGINT,
            previous_cash BIGINT
        )"""
        db = Database()
        db.execute_query(create_table_query)

        insert_stock_query = f"""
        INSERT INTO stock_fundamentals(
            ticker_name,
            current_price,
            pe_ratio,
            latest_revenue,
            latest_profit,
            latest_cash,
            previous_revenue,
            previous_profit,
            previous_cash
        )
        VALUES(
            '{analyzedStock.ticker}',
            {analyzedStock.current_price},
            {analyzedStock.pe_ratio},
            {analyzedStock.latest_revenue},
            {analyzedStock.latest_profit},
            {analyzedStock.latest_cash},
            {analyzedStock.previous_revenue},
            {analyzedStock.previous_profit},
            {analyzedStock.previous_cash}
        );
        """
        db.execute_query(insert_stock_query)

test =  Analyze()
#test.analyzeStock("GOOG")