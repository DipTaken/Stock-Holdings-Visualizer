import streamlit as st
import plotly.express as px
import pandas as pd
import calculations
import csv_parse

test_holdings = [['AMD', "Information Technology", 100.00, 0.00, False], 
                ['NVDA', "Information Technology", 50.00, 0.00, False], 
                ['INTC', "Information Technology", 150.00, 0.00, False],
                ['TD', "Financials", 200.00, 0.00, False],
                ['BMO', "Financials", 75.00, 0.00, False],
                ['GOOGL', "Communication Services", 300.00, 0.00, False],
                ['XEQT', "ETF", 2000.00, 0.00, False],
                ['XETM', "ETF", 2000.00, 0.00, False]]

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
    st.session_state.total_value = sum(holding[2] for holding in st.session_state.holdings)
if "num_stocks" not in st.session_state:
    st.session_state.num_stocks = 10


def launch_app():

    main_window()

def main_window():
    st.title("Holdings Visualizer")
    toggle_etf_holdings()
    st.selectbox("Sort by:", options=['Percentage', 'Alphabetical', 'Sector'], key='sort_option', width=200)
    st.number_input("Show stocks:", min_value=0, step=1, key='num_stocks')
    st.checkbox("Show ETF holdings", key='show_etf_holdings')
    # print("Holdings after sorting:" + str(st.session_state.current_holdings))
    st.write("You have a total of $" + (str(st.session_state.total_value)) + ".")
    # st.write(st.session_state)
    display_holdings()
    display_holdings_input()

def display_holdings():
    # print("Holdings:" + str(holdings))
    st.session_state.current_holdings = calculations.sort_holdings(st.session_state.current_holdings, st.session_state.sort_option)
    st.session_state.current_holdings = calculations.calculate_percentage(st.session_state.current_holdings)
    df = pd.DataFrame(st.session_state.current_holdings[:st.session_state.num_stocks], columns=["Holding", "Sector", "Amount", "Percentage", "Is ETF Stock"])
    bar_chart = px.bar(df,
                       x="Percentage",
                       y="Holding",
                       color="Sector",
                       category_orders={"Holding": df["Holding"].tolist()},
                       hover_data=["Holding", "Amount", "Percentage", "Sector"],
                       orientation='h')
    bar_chart.update_yaxes(type='category')
    bar_chart.update_layout(transition_duration=500)
    st.plotly_chart(bar_chart)

def display_holdings_input():
    # Dont want to display ETF holdings
    for holding in st.session_state.current_holdings:
        if not holding[4]:
            holding[2] = st.number_input(holding[0], 
                        min_value=0.00, 
                        value=holding[2], 
                        step=0.01,
                        key=holding[0])
        
        
def toggle_etf_holdings():
    if st.session_state.show_etf_holdings:
        st.session_state.current_holdings = st.session_state.holdings.copy()
        for holding in st.session_state.holdings:
            if holding[1] == "ETF":
                print("Holding:" + str(holding))
                toggle_individual_etf_holding(holding[0], holding[2])
    else:
        st.session_state.current_holdings = [h for h in st.session_state.holdings if not h[4]]
        
def toggle_individual_etf_holding(etf, value):
    etf_stocks= csv_parse.parse_csv(etf)
    merged = {h[0]: h for h in st.session_state.current_holdings if h[0] != etf}
    for stock in etf_stocks:
        ticker = stock[0]
        amount = stock[2] * 0.01 * value
        if ticker in merged:
            merged[ticker][2] += amount
        else:
            merged[ticker] = [ticker, stock[1], amount, 0.00, True]

    st.session_state.current_holdings = list(merged.values())
    
    