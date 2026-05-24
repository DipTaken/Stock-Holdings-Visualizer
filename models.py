from dataclasses import dataclass

MIN = 0.00

@dataclass
class Holding():
    ticker: str
    name: str
    sector: str
    amount: float
    percentage: float = MIN
    is_etf_stock: bool = False

@dataclass
class ETFStock():
    ticker: str
    name: str
    sector: str
    weight: float = MIN
