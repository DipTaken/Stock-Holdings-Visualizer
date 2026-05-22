import streamlit as st
import pandas as pd
import calculations

holdings = [['AMD', 100, 0], ['NVDA', 50, 0], ['INTC', 150, 0]]

def main_window():
    st.title("Holdings Visualizer")
    display_holdings(holdings)

def display_holdings(holdings):
    print("Holdings:" + str(holdings))
    holdings = calculations.calculate_percentage(holdings)
    df = pd.DataFrame(holdings, columns=["Holding", "Amount", "Percentage"])
    st.bar_chart(df, x="Holding", y="Percentage", horizontal=True)