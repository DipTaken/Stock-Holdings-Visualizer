import streamlit as st
import plotly.express as px
import pandas as pd

from calculations import calculate_percentage, calculate_total_value, sort_holdings
from csv_parse import parse_csv, ETF_NAME, ETF_TICKER, ETF_SECTOR, ETF_WEIGHT
    

"""
Holdings are in the form [ticker, name, sector, amount, percentage, is_etf_stock]
"""
test_holdings = [['AMD', "Advanced Micro Devices, Inc.", "Information Technology", 100.00, 0.00, False], 
                ['NVDA', "NVIDIA Corporation", "Information Technology", 50.00, 0.00, False], 
                ['INTC', "Intel Corporation", "Information Technology", 150.00, 0.00, False],
                ['TD', "Toronto-Dominion Bank", "Financials", 200.00, 0.00, False],
                ['BMO', "Bank of Montreal", "Financials", 75.00, 0.00, False],
                ['GOOGL', "Alphabet Inc.", "Communication Services", 300.00, 0.00, False],
                ['XEQT', "iShares Core S&P 500", "ETF", 2000.00, 0.00, False],
                ['XETM', "iShares S&P/TSX Energy Transition Mtrls Idx ETF", "ETF", 2000.00, 0.00, False]]

TICKER = 0
NAME = 1
SECTOR = 2
AMOUNT = 3
PERCENTAGE = 4
IS_ETF_STOCK = 5

if "current_holdings" not in st.session_state:
    st.session_state.current_holdings = []
if "holdings" not in st.session_state:
    st.session_state.holdings = test_holdings
if "etf_holdings" not in st.session_state:
    st.session_state.etf_holdings = []
if "sort_option" not in st.session_state:
    st.session_state.sort_option = 'Percentage'
if "show_etf_holdings" not in st.session_state:
    st.session_state.show_etf_holdings = False
if "total_value" not in st.session_state:
    st.session_state.total_value = calculate_total_value(st.session_state.holdings)
if "num_stocks" not in st.session_state:
    st.session_state.num_stocks = 10



def launch_app():
    main_window()

def main_window():
    st.title("Holdings Visualizer")
    toggle_etf_holdings()
    st.selectbox("Sort by:", options=['Percentage', 'Alphabetical', 'Sector'], key='sort_option', width=200)
    st.number_input("Show stocks:", min_value=0, step=1, key='num_stocks', placeholder=15, width=200)
    st.checkbox("Show ETF holdings", key='show_etf_holdings')
    # print("Holdings after sorting:" + str(st.session_state.current_holdings))
    st.write("You have a total of $" + (str(st.session_state.total_value)) + ".")
    # st.write(st.session_state)
    display_holdings()
    display_holdings_input()

def display_holdings():
    # print("Holdings:" + str(holdings))
    st.session_state.current_holdings = sort_holdings(st.session_state.current_holdings, st.session_state.sort_option)
    st.session_state.current_holdings = calculate_percentage(st.session_state.current_holdings)
    df = pd.DataFrame(st.session_state.current_holdings[:st.session_state.num_stocks], columns=["Holding", "Name", "Sector", "Amount", "Percentage", "Is ETF Stock"])
    bar_chart = px.bar(df,
                       x="Percentage",
                       y="Holding",
                       color="Sector",
                       category_orders={"Holding": df["Holding"].tolist()},
                       hover_data=["Holding", "Name","Amount", "Percentage", "Sector"],
                       orientation='h')
    bar_chart.update_yaxes(type='category')
    bar_chart.update_layout(transition_duration=500)
    st.plotly_chart(bar_chart)

def display_holdings_input():
    # Dont want to display ETF holdings
    for holding in st.session_state.current_holdings:
        if not holding[IS_ETF_STOCK]:
            holding[AMOUNT] = st.number_input(holding[TICKER] + " (" + holding[NAME] + ")", 
                        min_value=0.00, 
                        value=holding[AMOUNT], 
                        step=0.01,
                        key=holding[TICKER])
        
        
def toggle_etf_holdings():
    if st.session_state.show_etf_holdings:
        st.session_state.current_holdings = st.session_state.holdings.copy()
        for holding in st.session_state.holdings:
            if holding[SECTOR] == "ETF":
                print("Holding:" + str(holding))
                toggle_individual_etf_holding(holding[TICKER], holding[AMOUNT])
    else:
        st.session_state.current_holdings = [h for h in st.session_state.holdings if not h[IS_ETF_STOCK]]
def toggle_individual_etf_holding(etf, value):
    etf_stocks= parse_csv(etf)
    merged = {h[TICKER]: h for h in st.session_state.current_holdings if h[TICKER] != etf}
    for stock in etf_stocks:
        ticker = stock[ETF_TICKER]
        name = stock[ETF_NAME]
        amount = stock[ETF_WEIGHT] * 0.01 * value
        if ticker in merged:
            merged[ticker][AMOUNT] += amount
        else:
            merged[ticker] = [ticker, name, amount, 0.00, True]

    st.session_state.current_holdings = list(merged.values())
    
    