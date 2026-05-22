import csv
import io
from constants import AMOUNT, MIN
from csv_parse import parse_csv, CSV_TICKER, CSV_NAME, CSV_SECTOR, CSV_WEIGHT

def import_wealthsimple_csv(file):
    holdings = {}
    if file is not None:
        file = io.StringIO(file.getvalue().decode("utf-8"))
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 17 and row[0] != "Account Name": # Skip header row
                ticker = row[4]
                name = row[7]
                sector = find_sector(ticker)
                amount = row[17]
                percentage = MIN
                is_etf_stock = False
                if ticker not in holdings:
                    holdings[ticker] = [ticker, name, sector, float(amount), percentage, is_etf_stock]
                else:
                    holdings[ticker][AMOUNT] += float(amount)
    return list(holdings.values())

def find_sector(ticker):
    sector = check_if_known_sector(ticker)
    if sector != "NO DATA":
        return sector
    else:
        return check_if_known_etf(ticker)

def check_if_known_etf(ticker):
    try:
        with open(f'etf_holdings/{ticker}.csv', 'r') as f:
            return "ETF"
    except FileNotFoundError:
        return "NO DATA"

def check_if_known_sector(ticker):
    XEQT_holdings = parse_csv("XEQT")
    TEC_holdings = parse_csv("TEC")
    XETM_holdings = parse_csv("XETM")
    ETF_holdings = XEQT_holdings + TEC_holdings + XETM_holdings
    for holding in ETF_holdings:
        if holding [CSV_TICKER] == ticker:
            return holding[CSV_SECTOR]
    return "NO DATA"