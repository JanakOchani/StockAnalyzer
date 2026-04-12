from fastapi import FastAPI, HTTPException
from analyze import Analyze
from stock import Stock

stockAnalyzer = FastAPI()


@stockAnalyzer.get("/")
def root():
    return {"Hello": "StockAnalyzer"}


@stockAnalyzer.post("/analyze")
def analyzeStock(ticker: str):
    print(f"Ticker {ticker} received, will now analyze {ticker}.")
    analyze = Analyze()

    try:
        analyzeStock = analyze.analyzeStock(ticker)
        print(f"The ticker is {analyzeStock.ticker} and the price is {analyzeStock.current_price}")

        json_response = analyzeStock.getJSON()
        print(json_response)

        return json_response

    except Exception as error:
        print(f"Error is {error}.")
        return {"error": str(error)}