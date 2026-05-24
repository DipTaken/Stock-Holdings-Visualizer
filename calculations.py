from parsing.csv_parse import parse_csv
from models import Holding, MIN

def calculate_percentage(holdings):
    total_value = calculate_total_value(holdings)
    items = list(holdings.values())
    for holding in items:
        holding.percentage = round((holding.amount / total_value) * 100, 2) if total_value else 0.0
    return {h.ticker: h for h in items}

def sort_holdings(holdings, sort_option):
    items = list(holdings.values())
    if sort_option == 'Percentage':
        items.sort(key=lambda h: h.percentage, reverse=True)
    elif sort_option == 'Alphabetical':
        items.sort(key=lambda h: h.ticker)
    elif sort_option == 'Sector':
        items.sort(key=lambda h: h.percentage, reverse=True)
        items.sort(key=lambda h: h.sector)
    return {h.ticker: h for h in items}

def calculate_total_value(holdings):
    return round(sum(h.amount for h in list(holdings.values())), 2)

def expand_etf_into_current(etf, value, st_etf_holdings, st_current_holdings):
    # Cache ETF holdings to avoid re-parsing CSVs on every toggle
    if etf in st_etf_holdings:
        etf_stocks = st_etf_holdings[etf]
    else:
        etf_stocks = parse_csv(etf.split(".")[0])
        st_etf_holdings[etf] = etf_stocks
    
    merged = st_current_holdings
    for stock in etf_stocks.values(): # loop through stocks in the ETF and add them to current holdings
        amount = round(stock.weight * 0.01 * value, 2)
        if stock.ticker in merged:
            merged[stock.ticker].amount += amount
        else:
            merged[stock.ticker] = Holding(stock.ticker, stock.name, stock.sector, amount, MIN, True)

