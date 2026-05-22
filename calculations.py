def calculate_percentage(holdings):
    total_value = sum(holding[2] for holding in holdings)
    # print("Total value:" + str(total_value))
    for i, holding in enumerate(holdings):
        holdings[i][3] = round((holding[2] / total_value) * 100, 2)
        # print("Holding:" + str(holding) + " Percentage:" + str(holdings[i][3]))
    return holdings

def sort_holdings(holdings, sort_option):
    if sort_option == 'Percentage':
        holdings.sort(key=lambda x: x[3], reverse=True)
    elif sort_option == 'Alphabetical':
        holdings.sort(key=lambda x: x[0])
    elif sort_option == 'Sector':
        holdings.sort(key=lambda x: x[3], reverse=True)
        holdings.sort(key=lambda x: x[1])
    return holdings
    