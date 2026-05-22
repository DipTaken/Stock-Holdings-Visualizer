import streamlit as st
import plotly.express as px
import pandas as pd

from calculations import calculate_percentage, calculate_total_value, sort_holdings
from parsing.csv_parse import parse_csv
from constants import MIN, Holding, ETFStock
from parsing.wealthsimple_importer import import_wealthsimple_csv

test_holdings = [
    Holding('AMD', "Advanced Micro Devices, Inc.", "Information Technology", 100.00),
    Holding('NVDA', "NVIDIA Corporation", "Information Technology", 50.00),
    Holding('INTC', "Intel Corporation", "Information Technology", 150.00),
    Holding('TD', "Toronto-Dominion Bank", "Financials", 200.00),
    Holding('BMO', "Bank of Montreal", "Financials", 75.00),
    Holding('GOOGL', "Alphabet Inc.", "Communication Services", 300.00),
    Holding('XEQT', "iShares Core S&P 500", "ETF", 2000.00),
    Holding('XETM', "iShares S&P/TSX Energy Transition Mtrls Idx ETF", "ETF", 2000.00),
]

def launch_app():
    st.set_page_config(
        page_title="Stock Holdings Visualizer",
        layout="wide"
    )

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

    main_window()

def main_window():
    st.title("Stock Holdings Visualizer")
    sidebar()
    st.current_holdings = st.session_state.holdings.copy()
    st.session_state.total_value = calculate_total_value(st.session_state.current_holdings)
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
    st.session_state.current_holdings = calculate_percentage(st.session_state.current_holdings)
    st.session_state.current_holdings = sort_holdings(st.session_state.current_holdings, st.session_state.sort_option)
    rows = [
        (h.ticker, h.name, h.sector, h.amount, h.percentage, h.is_etf_stock)
        for h in st.session_state.current_holdings[:st.session_state.num_stocks]
    ]
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
        st.session_state.holdings = sort_holdings(st.session_state.holdings, st.session_state.sort_option)
        for holding in st.session_state.holdings:
            holding.amount = st.number_input(holding.ticker + " (" + holding.name + ")",
                        min_value=MIN,
                        value=holding.amount,
                        step=0.01,
                        width=300,
                        key=holding.ticker)

def toggle_etf_holdings():
    if st.session_state.show_etf_holdings:
        st.session_state.current_holdings = st.session_state.holdings.copy()
        for holding in st.session_state.holdings:
            if holding.sector == "ETF":
                toggle_individual_etf_holding(holding.ticker, holding.amount)
    else:
        st.session_state.current_holdings = [h for h in st.session_state.holdings if not h.is_etf_stock]

def toggle_individual_etf_holding(etf, value):
    etf_stocks = parse_csv(etf)
    merged = {h.ticker: h for h in st.session_state.current_holdings if h.ticker != etf}
    for stock in etf_stocks:
        amount = round(stock.weight * 0.01 * value, 2)
        if stock.ticker in merged:
            merged[stock.ticker].amount += amount
        else:
            merged[stock.ticker] = Holding(stock.ticker, stock.name, stock.sector, amount, MIN, True)

    st.session_state.current_holdings = list(merged.values())
