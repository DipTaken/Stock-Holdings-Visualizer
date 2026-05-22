MIN = 0.00

"""Holdings list format:
[ticker, name, sector, amount, percentage, is_etf_stock]
"""
TICKER = 0
NAME = 1
SECTOR = 2
AMOUNT = 3
PERCENTAGE = 4
IS_ETF_STOCK = 5

"""ETF Holdings list format:
[ticker, name, sector, percentage]
"""
CSV_TICKER = 0
CSV_NAME = 1
CSV_SECTOR = 2
CSV_WEIGHT = 3