from fastapi import FastAPI, HTTPException
import yfinance as yf
import psycopg2

app = FastAPI()

def getDBConnection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="your_db_name",
            user="your_username",
            password="your_password"
        )
        return connection
    except Exception as problem:
        print(f"There was problem getting connection {problem}")


#FIRST API CONSTRUCTION
@app.post("/analyze")
def analyze_stock(ticker):
    try:
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)

        info = stock.info
        financials = stock.financials
        balance = stock.balance_sheet

        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        trailing_pe = info.get('trailingPE')
        company_name = info.get('longName', ticker)

        latest_revenue = financials.loc['Total Revenue'].iloc[0] if 'Total Revenue' in financials.index else None
        latest_profit = financials.loc['Net Income'].iloc[0] if 'Net Income' in financials.index else None
        latest_cash = balance.loc['Cash'].iloc[0] if 'Cash' in balance.index else None

        previous_revenue = financials.loc['Total Revenue'].iloc[1] if len(financials.columns) > 1 else None
        previous_profit = financials.loc['Net Income'].iloc[1] if len(financials.columns) > 1 else None
        previous_cash = balance.loc['Cash'].iloc[1] if len(balance.columns) > 1 else None

        profit_growth_pct = None
        if latest_profit and previous_profit and previous_profit != 0:
            profit_growth_pct = round(((latest_profit - previous_profit) / previous_profit) * 100, 2)
        if trailing_pe is None or profit_growth_pct is None:
            verdict = "Fair"
            reason = "Not enough data"
        elif trailing_pe < 22 and profit_growth_pct > 12:
            verdict = "Not so expensive"
            reason = f"Good profit growth ({profit_growth_pct}%) with reasonable PE."
        elif trailing_pe > 35:
            verdict = "Looks expensive"
            reason = f"High PE ratio ({trailing_pe})."
        else:
            verdict = "Fairly valued"
            reason = f"PE is {trailing_pe} and profit growth is {profit_growth_pct}%."

        result = {
            "ticker": ticker,
            "company_name": company_name,
            "current_price": current_price,
            "trailing_pe": trailing_pe,
            "profit_growth_pct": profit_growth_pct,
            "valuation_verdict": verdict,
            "reason": reason
        }

        #THEN WE MAKE THE CONNECTION STUFF
        try:
            connection = getDBConnection()
            sqlEditor = connection.cursor()

            query = f"""
            INSERT INTO stock_fundamentals (
                ticker,
                current_price,
                trailing_pe,
                latest_revenue,
                latest_profit,
                latest_cash,
                previous_revenue,
                previous_profit,
                previous_cash,
                profit_growth_pct,
                valuation_verdict,
                reason
            )
            VALUES (
                '{ticker}',
                {current_price},
                {trailing_pe},
                {latest_revenue},
                {latest_profit},
                {latest_cash},
                {previous_revenue},
                {previous_profit},
                {previous_cash},
                {profit_growth_pct},
                '{verdict}',
                '{reason}'
            );
            """

            sqlEditor.execute(query)
            connection.commit()

            sqlEditor.close()
            connection.close()
            print("PostgreSQL connection is closed")

        except Exception as error:
            print("Error while connecting to PostgreSQL:", error)

        return result

    except Exception as error:
        raise HTTPException(status_code=404, detail="Stock not found or error fetching data")


#SECOND API CONSTRUCTION
@app.get("/stocks")
def get_stocks():
    try:
        connection = getDBConnection()
        sqlEditor = connection.cursor()

        query = """
        SELECT 
            ticker,
            analysis_date,
            current_price,
            trailing_pe,
            profit_growth_pct,
            valuation_verdict,
            reason
        FROM stock_fundamentals;;
        """

        sqlEditor.execute(query)
        rows = sqlEditor.fetchall()

        results = []
        for row in rows:
            results.append({
                "ticker": row[0],
                "analysis_date": row[1],
                "current_price": row[2],
                "trailing_pe": row[3],
                "profit_growth_pct": row[4],
                "valuation_verdict": row[5],
                "reason": row[6]
            })

        sqlEditor.close()
        connection.close()
        print("PostgreSQL connection is closed")
        return results

    except Exception as error:
        print("Error while fetching stocks:", error)
        raise HTTPException(status_code=500, detail="Error fetching stocks")