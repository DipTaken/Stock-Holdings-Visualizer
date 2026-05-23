import yfinance as yf

def search_yfinance(ticker):
    results = yf.Search(ticker, max_results=10, news_count=0, lists_count=0).quotes
    return results

print(search_yfinance("PNG"))