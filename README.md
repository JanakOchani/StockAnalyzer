This is an API written in FastAPI which performs fundamental analysis of stocks by taking real-time data about a specific stock from yfinance. 
User needs to enter the ticker of the stock, and the API will return the following financial metrics: current stock price, its P/E ratio, 
its revenue, net profit, and cash flows. 
Moreover, the program also compares data of the last year with previous years' data to calculate profit percentage growth. 
Finally, a stock valuation verdict is calculated ("Not so expensive", "Fairly valued", or "Looks expensive").

The codebase of this project consists of four modules. 
The first one is a python file api.py with http methods implemented in it and a specific route /analyze. 
The second module is the code file analyze.py with methods of retrieving data from yfinance library, making some calculations, 
and saving results in the database. 
The third module is a python file stock.py where the class Stock is defined, and all the necessary attributes for the financial analysis are set. 
The fourth module database.py is about managing the connection to PostgreSQL and executing SQL queries.

Commands:

Bring up web server: 
uvicorn api:stockAnalyzer --reload


Run API 
curl -X POST "http://127.0.0.1:8000/analyze?ticker=AMZN"





