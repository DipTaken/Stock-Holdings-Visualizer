import csv
import os

from models import ETFStock

etf_holdings_path = './etf_holdings'

def parse_csv(file_name):
    file_path = os.path.join(etf_holdings_path, f"{file_name}.csv")
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        holdings = {}
        for row in reader:
            if (len(row) >= 6 and row[5] != "Weight (%)" and float(row[5]) > 0.00):
                holdings[row[0]] = ETFStock(row[0], row[1], row[2], float(row[5]))
    return dict(list(holdings.items())[:100])
