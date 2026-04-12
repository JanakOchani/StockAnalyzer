from fastapi import FastAPI, HTTPException

stockAnalyzer = FastAPI()



@stockAnalyzer.get("/")
def root():
    return {"Hello": "StockAnalyzer"}

@stockAnalyzer.post("/analyze")
def analyzeStock(ticker : str):
    print("test")
    return {"ticker": {ticker}}