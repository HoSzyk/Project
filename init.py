import sqlite3
from view import start

if __name__ == '__main__':
    conn = sqlite3.connect('Data/database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS currency_stats (
        symbol TEXT,
        date INTEGER,
        value REAL,
        PRIMARY KEY (symbol, date)
    )''')
    c.close()
    start()
