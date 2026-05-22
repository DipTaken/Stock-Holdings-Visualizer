import csv
import os

from constants import ETFStock

etf_holdings_path = './etf_holdings'

def parse_csv(file_name):
    file_path = find_file(file_name, etf_holdings_path)
    if not file_path:
        return {}
    file = open(file_path)
    reader = csv.reader(file)
    holdings = {}
    for row in reader:
        if (len(row) >= 6 and row[5] != "Weight (%)" and float(row[5]) > 0.00):
            holdings[row[0]] = ETFStock(row[0], row[1], row[2], float(row[5]))
    return {h.ticker: h for h in list(holdings.values())[:100]}

def find_file(file_name, directory):
    for root, dirs, files in os.walk(directory):
        if f"{file_name}.csv" in files:
            return os.path.join(root, f"{file_name}.csv")
    return None
