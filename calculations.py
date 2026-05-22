def calculate_percentage(holdings):
    total_value = calculate_total_value(holdings)
    for holding in holdings:
        holding.percentage = round((holding.amount / total_value) * 100, 2) if total_value else 0.0
    return holdings

def sort_holdings(holdings, sort_option):
    if sort_option == 'Percentage':
        holdings.sort(key=lambda h: h.percentage, reverse=True)
    elif sort_option == 'Alphabetical':
        holdings.sort(key=lambda h: h.ticker)
    elif sort_option == 'Sector':
        holdings.sort(key=lambda h: h.percentage, reverse=True)
        holdings.sort(key=lambda h: h.sector)
    return holdings

def calculate_total_value(holdings):
    return sum(h.amount for h in holdings)
