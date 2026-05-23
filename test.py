import yfinance as yf

def search_yfinance(ticker):
    results = yf.Search(ticker, max_results=10, news_count=0, lists_count=0).quotes
    return results

#we could use this to find "UNKNOWN" sectors
res = search_yfinance("PNG")
info = yf.Ticker(res[0]['symbol']).info
print(info)