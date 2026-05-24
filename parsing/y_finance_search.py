import yfinance as yf
import streamlit as st

@st.cache_data(show_spinner=False, ttl=3600)
def search_yfinance(query):
    if not query:
        return []
    try:
        rows = yf.Search(query, max_results=50, news_count=0, lists_count=0, enable_fuzzy_query=True).quotes
    except Exception:
        return []
    result_list = []
    for r in rows:
        if ((r.get("quoteType", "") not in ["EQUITY", "ETF"] or r.get("exchange") not in ["NMS", "NYQ", "TOR", "CNQ", "NEO", "VAN"]) 
            and r.get("currency") != "CAD"): #Remove this line after we implement currency conversion
            continue
        ticker = r.get("symbol", "")
        name = r.get("shortname", "")
        sector = r.get("sector") or ("ETF" if r.get("quoteType") == "ETF" else "Unknown")
        result_list.append((f"{ticker} - {name}", f"{ticker}|{name}|{sector}"))
    return result_list