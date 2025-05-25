import sqlite3

class ExecuteQuery:
    def __init__(self, query, params):
        self.query = query
        self.params = params
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect('test.db')
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

if __name__ == "__main__":
    
    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30), ('Bob', 25), ('Charlie', 35)")
        conn.commit()

   
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(query, params) as results:
        print(results)
