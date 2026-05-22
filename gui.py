import streamlit as st
import plotly.express as px
import pandas as pd

from calculations import calculate_percentage, calculate_total_value, sort_holdings
from csv_parse import parse_csv
from constants import MIN, TICKER, NAME, SECTOR, AMOUNT, PERCENTAGE, IS_ETF_STOCK, CSV_TICKER, CSV_NAME, CSV_SECTOR, CSV_WEIGHT
from wealthsimple_importer import import_wealthsimple_csv

"""
Holdings are in the form [ticker, name, sector, amount, percentage, is_etf_stock]
"""
test_holdings = [['AMD', "Advanced Micro Devices, Inc.", "Information Technology", 100.00, MIN, False], 
                ['NVDA', "NVIDIA Corporation", "Information Technology", 50.00, MIN, False], 
                ['INTC', "Intel Corporation", "Information Technology", 150.00, MIN, False],
                ['TD', "Toronto-Dominion Bank", "Financials", 200.00, MIN, False],
                ['BMO', "Bank of Montreal", "Financials", 75.00, MIN, False],
                ['GOOGL', "Alphabet Inc.", "Communication Services", 300.00, MIN, False],
                ['XEQT', "iShares Core S&P 500", "ETF", 2000.00, MIN, False],
                ['XETM', "iShares S&P/TSX Energy Transition Mtrls Idx ETF", "ETF", 2000.00, MIN, False]]

if "current_holdings" not in st.session_state:
    st.session_state.current_holdings = []
if "holdings" not in st.session_state:
    st.session_state.holdings = test_holdings
if "sort_option" not in st.session_state:
    st.session_state.sort_option = 'Percentage'
if "show_etf_holdings" not in st.session_state:
    st.session_state.show_etf_holdings = False
if "total_value" not in st.session_state:
    st.session_state.total_value = calculate_total_value(st.session_state.holdings)
if "num_stocks" not in st.session_state:
    st.session_state.num_stocks = 10

def launch_app():
    st.set_page_config(
        page_title="Stock Holdings Visualizer",
        layout="wide"
    )
    main_window()

def main_window():
    st.title("Stock Holdings Visualizer")
    sidebar()
    st.write("You have a total of $" + (str(st.session_state.total_value)) + ".")
    toggle_etf_holdings()
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        display_holdings()
    with col2:
        st.subheader("Edit Holdings")
        display_holdings_input()
    
def sidebar():
    with st.sidebar:
        st.write("Configuration")
        st.selectbox("Sort by:", options=['Percentage', 'Alphabetical', 'Sector'], key='sort_option', width=200)
        st.number_input("Show stocks:", min_value=0, max_value=100, step=1, key='num_stocks', placeholder=15, width=100)
        st.checkbox("Show ETF holdings", key='show_etf_holdings')
        st.file_uploader("Import Wealthsimple CSV", type="csv", on_change=load_holdings, key="ws_csv")

def load_holdings():
    st.session_state.holdings = import_wealthsimple_csv(st.session_state.ws_csv)
    st.session_state.total_value = calculate_total_value(st.session_state.holdings)
    st.session_state.current_holdings = st.session_state.holdings.copy()
    
def display_holdings():
    # print("Holdings:" + str(holdings))
    st.session_state.current_holdings = calculate_percentage(st.session_state.current_holdings)
    st.session_state.current_holdings = sort_holdings(st.session_state.current_holdings, st.session_state.sort_option)
    df = pd.DataFrame(st.session_state.current_holdings[:st.session_state.num_stocks], columns=["Holding", "Name", "Sector", "Amount", "Percentage", "Is ETF Stock"])
    bar_chart = px.bar(df,
                       x="Percentage",
                       y="Holding",
                       color="Sector",
                       category_orders={"Holding": df["Holding"].tolist()},
                       hover_data=["Holding", "Name","Amount", "Percentage", "Sector"],
                       orientation='h',
                       height=700,
                       width=800)
    bar_chart.update_yaxes(type='category')
    bar_chart.update_layout(transition_duration=500)
    st.plotly_chart(bar_chart)

def display_holdings_input():
    with st.container(height=500):
        for holding in st.session_state.holdings:
            holding[AMOUNT] = st.number_input(holding[TICKER] + " (" + holding[NAME] + ")",
                        min_value=MIN,
                        value=holding[AMOUNT],
                        step=0.01,
                        width=300,
                        key=holding[TICKER])
        
def toggle_etf_holdings():
    if st.session_state.show_etf_holdings:
        st.session_state.current_holdings = st.session_state.holdings.copy()
        for holding in st.session_state.holdings:
            if holding[SECTOR] == "ETF":
                # print("Holding:" + str(holding))
                toggle_individual_etf_holding(holding[TICKER], holding[AMOUNT])
    else:
        st.session_state.current_holdings = [h for h in st.session_state.holdings if not h[IS_ETF_STOCK]]
        
def toggle_individual_etf_holding(etf, value):
        etf_stocks= parse_csv(etf)
        merged = {h[TICKER]: h for h in st.session_state.current_holdings if h[TICKER] != etf}
        for stock in etf_stocks:
            ticker = stock[CSV_TICKER]
            name = stock[CSV_NAME]
            sector = stock[CSV_SECTOR]
            amount = round(stock[CSV_WEIGHT] * 0.01 * value, 2)
            if ticker in merged:
                merged[ticker][AMOUNT] += amount
            else:
                merged[ticker] = [ticker, name, sector, amount, MIN, True]

        st.session_state.current_holdings = list(merged.values())    