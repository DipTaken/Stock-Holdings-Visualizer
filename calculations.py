def calculate_percentage(holdings):
    total_value = calculate_total_value(holdings)
    items = list(holdings.values())
    for holding in items:
        holding.percentage = round((holding.amount / total_value) * 100, 2) if total_value else 0.0
    return {h.ticker: h for h in items}

def sort_holdings(holdings, sort_option):
    items = list(holdings.values())
    if sort_option == 'Percentage':
        items.sort(key=lambda h: h.percentage, reverse=True)
    elif sort_option == 'Alphabetical':
        items.sort(key=lambda h: h.ticker)
    elif sort_option == 'Sector':
        items.sort(key=lambda h: h.percentage, reverse=True)
        items.sort(key=lambda h: h.sector)
    return {h.ticker: h for h in items}

def calculate_total_value(holdings):
    return round(sum(h.amount for h in list(holdings.values())), 2)
