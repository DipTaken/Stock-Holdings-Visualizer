# Holdings Visualizer

A Streamlit web app for visualizing a personal investment portfolio as an interactive bar chart, with the ability to drill into ETF holdings so the underlying stocks are merged into the rest of the portfolio.

## Try it here
https://diptaken-stockvisualizer.streamlit.app/

## Features

- Interactive horizontal bar chart of your holdings, colored by sector (Plotly).
- Edit holding values inline — the chart updates in real time.
- Sort by **Percentage**, **Alphabetical**, or **Sector**.
- Limit the number of stocks shown.
- Toggle "Show ETF holdings" to expand each ETF into its underlying stocks (weighted by the ETF's allocation) and merge them with your existing direct positions.

## Requirements

- Python 3.12+
- `streamlit`
- `plotly`
- `pandas`

Install dependencies:

```bash
pip install streamlit plotly pandas
```

## Running

From the project root:

```bash
streamlit run main.py
```

This launches the app in your browser.

## Project Structure

- [main.py](main.py) — entry point; launches the Streamlit app.
- [gui.py](gui.py) — Streamlit UI, session state, and chart rendering.
- [calculations.py](calculations.py) — percentage and sorting logic.
- [csv_parse.py](csv_parse.py) — reads ETF holdings CSVs from [etf_holdings/](etf_holdings/).
- [etf_holdings/](etf_holdings/) — CSV files containing per-ETF holdings data (e.g. `XEQT.csv`, `XETM.csv`, `TEC.csv`, `CHPS.csv`).

## Holdings Format

Holdings are stored in session state as a list of rows with the following columns:

| Index | Field         | Example                  |
|-------|---------------|--------------------------|
| 0     | Ticker        | `"AMD"`                  |
| 1     | Sector        | `"Information Technology"` |
| 2     | Amount ($)    | `100.00`                 |
| 3     | Percentage    | `0.00` (computed)        |
| 4     | Is ETF Stock  | `False`                  |

The app currently boots with a hard-coded `test_holdings` list in [gui.py](gui.py); edit it there to seed your own portfolio.

## Adding a New ETF

1. Drop the ETF's holdings CSV into [etf_holdings/](etf_holdings/), named `<TICKER>.csv` (e.g. `XEQT.csv`).
2. The CSV must follow the iShares-style format: a header row, then rows with at least 25 columns where column 0 is the ticker, column 1 is the name, column 2 is the sector, and column 5 is the weight (%).
3. Add the ETF to `test_holdings` in [gui.py](gui.py) with sector `"ETF"`.

See [etf_holdings/updated.md](etf_holdings/updated.md) for notes on the bundled datasets — `TEC` and `CHPS` were AI-reformatted, so treat them with caution.
