from gui import TICKER, NAME, SECTOR, AMOUNT, PERCENTAGE, IS_ETF_STOCK

def calculate_percentage(holdings):
    total_value = calculate_total_value(holdings)
    # print("Total value:" + str(total_value))
    for i, holding in enumerate(holdings):
        holdings[i][PERCENTAGE] = round((holding[AMOUNT] / total_value) * 100, 2)
        # print("Holding:" + str(holding) + " Percentage:" + str(holdings[i][PERCENTAGE]))
    return holdings

def sort_holdings(holdings, sort_option):
    if sort_option == 'Percentage':
        holdings.sort(key=lambda x: x[PERCENTAGE], reverse=True)
    elif sort_option == 'Alphabetical':
        holdings.sort(key=lambda x: x[TICKER])
    elif sort_option == 'Sector':
        holdings.sort(key=lambda x: x[SECTOR])
        holdings.sort(key=lambda x: x[PERCENTAGE], reverse=True)
    return holdings

def calculate_total_value(holdings):
    return sum(holding[AMOUNT] for holding in holdings)