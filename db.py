import sqlite3
from models import Holding

def init_db():
    con = sqlite3.connect("holdings.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS holdings 
                (UUID TEXT,
                ticker TEXT,
                name TEXT, 
                sector TEXT, 
                amount REAL,
                PRIMARY KEY (UUID, ticker))''')
    con.commit()
    con.close()
    
def save_holdings(holdings, UUID):
    con = sqlite3.connect("holdings.db")
    cur = con.cursor()
    cur.execute("DELETE FROM holdings WHERE UUID = ?", (UUID,))
    for ticker, holding in holdings.items():
        cur.execute(
            "INSERT INTO holdings (UUID, ticker, name, sector, amount) VALUES (?, ?, ?, ?, ?)",
            (UUID, ticker, holding.name, holding.sector, holding.amount)
        )
    con.commit()
    con.close()
    
def load_holdings(UUID):
    con = sqlite3.connect("holdings.db")
    cur = con.cursor()
    cur.execute('''SELECT ticker, name, sector, amount FROM holdings WHERE UUID = ?''', (UUID,))
    rows = cur.fetchall()
    if rows == []:
        return None
    holdings = {}
    for row in rows:
        ticker = row[0]
        name = row[1]
        sector = row[2]
        amount = row[3]
        holdings[ticker] = Holding(ticker, name, sector, amount)
    con.close()
    return holdings