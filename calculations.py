def calculate_percentage(holdings):
    total_value = sum(holding[1] for holding in holdings)
    print("Total value:" + str(total_value))
    for i, holding in enumerate(holdings):
        holdings[i][2] = (holding[1] / total_value) * 100
        print("Holding:" + str(holding) + " Percentage:" + str(holdings[i][2]))
    return holdings
