import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS currency_stats (
        symbol TEXT PRIMARY KEY,
        date INTEGER,
        value REAL
    )''')
    c.close()
