import psycopg2

class Database:
    def __init__(self):
        print("Database object was created.")

    def execute_query(self, query):
        try:
            print(query)

            connection = psycopg2.connect(
                host='localhost',
                port='5432',
                database='stock_fundamentals',
                user='postgres',
                password='postgres'
            )

            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            print("Query executed and connection closed successfully.")

        except Exception as my_error:
            print(f"Error that was given: {my_error}")
