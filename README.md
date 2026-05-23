# Holdings Visualizer

A Streamlit web app for visualizing a personal investment portfolio as an interactive bar chart, with the ability to drill into ETF holdings so the underlying stocks are merged into the rest of the portfolio.

## Try it here
https://diptaken-stockvisualizer.streamlit.app/

## Features

- Interactive horizontal bar chart of your holdings, colored by sector (Plotly).
- Search for stocks or ETFs by ticker or company name and add them directly to your portfolio.
- Edit holding values inline — the chart updates in real time.
- Remove any holding with one click.
- Sort by **Percentage**, **Alphabetical**, or **Sector**.
- Limit the number of stocks shown.
- Filter out stocks below a minimum portfolio percentage.
- Toggle "Show ETF holdings" to expand each ETF into its underlying stocks (weighted by the ETF's allocation) and merge them with your existing direct positions.
- Import your portfolio directly from a Wealthsimple activity CSV.

## Requirements

- Python 3.12+
- `streamlit`
- `plotly`
- `pandas`
- `yfinance`
- `streamlit-searchbox`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running

From the project root:

```bash
streamlit run main.py
```

This launches the app in your browser.

## Importing from Wealthsimple

The sidebar has an **Import Wealthsimple CSV** uploader that will populate your holdings from a Wealthsimple activity export.

### Getting your CSV from Wealthsimple

The CSV export option is **only available on the desktop website** — the mobile app does not expose it.

1. Open a desktop browser and sign in at [my.wealthsimple.com](https://my.wealthsimple.com).
2. Open the account you want to export (e.g. your TFSA or non-registered account).
3. Go to the **Activity** tab for that account.
4. Click the **download / export** icon (usually near the top of the activity list) and choose **CSV**.
5. Save the file locally, then upload it via the sidebar uploader in the app.

If you have multiple Wealthsimple accounts, export each one separately and upload them one at a time — each import replaces the current holdings.

## Project Structure

- [main.py](main.py) — entry point; launches the Streamlit app.
- [gui.py](gui.py) — Streamlit UI, session state, and chart rendering.
- [calculations.py](calculations.py) — percentage and sorting logic.
- [constants.py](constants.py) — `Holding` and `ETFStock` dataclasses and shared constants.
- [parsing/csv_parse.py](parsing/csv_parse.py) — reads ETF holdings CSVs from [etf_holdings/](etf_holdings/).
- [parsing/wealthsimple_importer.py](parsing/wealthsimple_importer.py) — parses a Wealthsimple activity CSV into `Holding` objects.
- [etf_holdings/](etf_holdings/) — CSV files containing per-ETF holdings data (e.g. `XEQT.csv`, `XETM.csv`, `TEC.csv`, `CHPS.csv`, `ZGD.csv`, `XEG.csv`, `XIU.csv`, `QQC.csv`).

## Holdings Format

Holdings are stored in session state as a `dict[ticker, Holding]`. The `Holding` dataclass (defined in [constants.py](constants.py)) has the following fields:

| Field        | Type    | Example                      |
|--------------|---------|------------------------------|
| ticker       | `str`   | `"AMD"`                      |
| name         | `str`   | `"Advanced Micro Devices"`   |
| sector       | `str`   | `"Information Technology"`   |
| amount       | `float` | `100.00`                     |
| percentage   | `float` | `0.00` (computed)            |
| is_etf_stock | `bool`  | `False`                      |

The app boots with a hard-coded `test_holdings` dict in [gui.py](gui.py); edit it there to seed your own portfolio.

## Adding a New ETF

1. Drop the ETF's holdings CSV into [etf_holdings/](etf_holdings/), named `<TICKER>.csv` (e.g. `XEQT.csv`).
2. The CSV must follow the iShares-style format: a header row, then rows with at least 25 columns where column 0 is the ticker, column 1 is the name, column 2 is the sector, and column 5 is the weight (%).
3. Add the ETF to `test_holdings` in [gui.py](gui.py) with sector `"ETF"`.

See [etf_holdings/updated.md](etf_holdings/updated.md) for notes on when the bundled datasets were last refreshed.
