import streamlit as st
import plotly.express as px
import pandas as pd
import uuid

from streamlit_searchbox import st_searchbox
from calculations import calculate_percentage, calculate_total_value, sort_holdings, expand_etf_into_current
from db import init_db, save_holdings, load_holdings
from models import MIN, Holding
from parsing.wealthsimple_importer import import_wealthsimple_csv
from parsing.y_finance_search import search_yfinance
from dataclasses import replace
from copy import deepcopy

test_holdings = {
    "AMD": Holding('AMD', "Advanced Micro Devices, Inc.", "Information Technology", 500.00),
    "BMO": Holding('BMO', "Bank of Montreal", "Financials", 250.00),
    "GOOGL": Holding('GOOGL', "Alphabet Inc.", "Communication Services", 1000.00),
    "XEQT": Holding('XEQT', "iShares Core S&P 500", "ETF", 4000.00),
    "XETM": Holding('XETM', "iShares S&P/TSX Energy Transition Mtrls Idx ETF", "ETF", 2000.00),
    "TEC": Holding('TEC', "TD Global Technology Leaders Index ETF", "ETF", 2000.00),
}

def launch_app():
    st.set_page_config(
        page_title="Stock Holdings Visualizer",
        layout="wide"
    )
    init_db()
    initialize_session_state()
    main_window()
    
def initialize_session_state():
    if "UUID" not in st.session_state:
        if "UUID" in st.query_params:
            st.session_state.UUID = st.query_params["UUID"]
        else:
            st.session_state.UUID = str(uuid.uuid4())
    st.query_params["UUID"] = st.session_state.UUID
    if "current_holdings" not in st.session_state:
        st.session_state.current_holdings = {}
    if "holdings" not in st.session_state:
        st.session_state.holdings = load_holdings(st.session_state.UUID) or {}
    if "sort_option" not in st.session_state:
        st.session_state.sort_option = 'Percentage'
    if "show_etf_holdings" not in st.session_state:
        st.session_state.show_etf_holdings = False
    if "total_value" not in st.session_state:
        st.session_state.total_value = 0.00
    if "num_stocks" not in st.session_state:
        st.session_state.num_stocks = 10
    if "etf_holdings" not in st.session_state:
        st.session_state.etf_holdings = {}
    if "loading_message" not in st.session_state:
        st.session_state.loading_message = ""
    if "search_query_n" not in st.session_state:
        st.session_state.search_query_n = 0

def main_window():
    st.subheader("Visualize your stock portfolio and its diversification. (Only Canadian listings for now)")
    sidebar()
    total_placeholder = st.empty()
    col_graph, col_holdings = st.columns([0.7, 0.3])
    with col_holdings: 
        holdings_column()
    st.session_state.total_value = calculate_total_value(st.session_state.holdings)
    total_placeholder.write(f"You have a total of ${round(st.session_state.total_value, 2)}.")
    toggle_etf_holdings()
    with col_graph:
        display_holdings()

def sidebar():
    with st.sidebar:
        st.title("Stock Holdings Visualizer")
        st.write("Configuration")
        st.selectbox("Sort by:", options=['Percentage', 'Alphabetical', 'Sector'], key='sort_option', width=200)
        st.number_input("Show stocks:", min_value=0, max_value=100, step=1, key='num_stocks', placeholder=15, width=100)
        st.number_input("Don't display stocks with less than %:", min_value=MIN, max_value=100.00, step=0.01, key='min_percentage', placeholder=0.5, width=300)
        st.checkbox("Show ETF holdings", key='show_etf_holdings')
        st.file_uploader("Import Wealthsimple CSV", type="csv", on_change=load_holdings_from_wealthsimple, key="ws_csv")
        st.text_input("Manual load? (Enter UUID)", key="manual_load_uuid")
        if st.button("Load UUID"):
            manual_load()
        st.write("Your portfolio UUID is: " + st.session_state.UUID)
        st.write("Status: " + st.session_state.loading_message)

def holdings_column():
    st.subheader("Edit Holdings")
    search_bar()
    display_holdings_input()
    col_reset, col_default = st.columns(2)
    with col_reset:
        if st.button("Reset to empty"):
            st.session_state.holdings = {}
            save_current_holdings()
            st.rerun()
    with col_default:
        if st.button("Example portfolio"):
            st.session_state.holdings = deepcopy(test_holdings)
            save_current_holdings()
            st.rerun() 

def manual_load():
    input_uuid = st.session_state.manual_load_uuid
    if input_uuid:
        loaded = load_holdings(input_uuid)
        if loaded is not None:
            st.session_state.holdings = loaded
            st.session_state.UUID = input_uuid
            st.session_state.total_value = calculate_total_value(st.session_state.holdings)
            st.session_state.loading_message = "loaded portfolio with UUID " + input_uuid
        else:
            st.session_state.loading_message = "no portfolio found with UUID " + input_uuid

def load_holdings_from_wealthsimple():
    st.session_state.holdings = import_wealthsimple_csv(st.session_state.ws_csv)
    st.session_state.total_value = calculate_total_value(st.session_state.holdings)
    save_holdings(st.session_state.holdings, st.session_state.UUID)

def search_bar():
    selection = st_searchbox(search_yfinance,
                             label="Search for stocks",
                             placeholder="Type a ticker or company name...",
                             key=f"search_query_{st.session_state.search_query_n}")
    if selection is not None:
        ticker, name, sector = selection.split("|", 2)
        ticker = ticker.split(".", 1)[0] # remove .TO ticker suffix if it exists
        if ticker not in st.session_state.holdings:
            add_stock(ticker, name, sector)
        st.session_state.search_query_n += 1 # Force the search box to reset after each selection by changing its key
        st.rerun()

def add_stock(ticker, name, sector):
    st.session_state.holdings[ticker] = Holding(ticker, name, sector, 0.00)
    save_current_holdings()

def save_current_holdings():
    save_holdings(st.session_state.holdings, st.session_state.UUID)

def display_holdings():
    st.session_state.current_holdings = calculate_percentage(st.session_state.current_holdings)
    st.session_state.current_holdings = sort_holdings(st.session_state.current_holdings, st.session_state.sort_option)
    
    rows = [
        (h.ticker, h.name, h.sector, h.amount, h.percentage, h.is_etf_stock)
        for h in list(st.session_state.current_holdings.values()) 
        if h.percentage >= st.session_state.min_percentage
    ][:st.session_state.num_stocks]
    
    df = pd.DataFrame(rows, columns=["Holding", "Name", "Sector", "Amount", "Percentage", "Is ETF Stock"])
    bar_chart = px.bar(df,
                       x="Percentage",
                       y="Holding",
                       color="Sector",
                       text="Percentage",
                       category_orders={"Holding": df["Holding"].tolist()},
                       hover_data=["Holding", "Name", "Amount", "Percentage", "Sector"],
                       orientation='h',
                       height=700,
                       width=600)
    bar_chart.update_yaxes(type='category')
    bar_chart.update_xaxes(range=[0, 100])
    st.plotly_chart(bar_chart)

def display_holdings_input():
    with st.container(height=500):
        st.session_state.holdings = sort_holdings(st.session_state.holdings, st.session_state.sort_option) # sort holdings in input section as well for consistency
        for ticker, holding in list(st.session_state.holdings.items()):
            if not holding.is_etf_stock: # only allow editing of non-ETF stocks in the input section
                col1, col2 = st.columns([0.8, 0.2], vertical_alignment="bottom")
                with col1: # display ticker and name, and allow editing of amount
                    holding.amount = st.number_input(holding.ticker + " (" + holding.name + ")",
                            min_value=MIN,
                            value=holding.amount,
                            step=0.01,
                            width=300,
                            on_change=save_current_holdings)
                with col2: # button to remove the stock from holdings
                    if st.button("X", key=f"remove_{ticker}", width=50):
                        del st.session_state.holdings[holding.ticker]
                        save_current_holdings()
                        st.rerun()

def toggle_etf_holdings():

    if st.session_state.show_etf_holdings: # if the toggle is on, expand ETF holdings into current holdings
        st.session_state.current_holdings = {
        ticker: replace(h) for ticker, h in st.session_state.holdings.items() 
                            if h.sector != "ETF"
        }
        for holding in st.session_state.holdings.values():
            if holding.sector == "ETF":
                expand_etf_into_current(holding.ticker, holding.amount, st.session_state.etf_holdings, st.session_state.current_holdings)
    else:
        st.session_state.current_holdings = {
            ticker: replace(h) for ticker, h in st.session_state.holdings.items()
        }