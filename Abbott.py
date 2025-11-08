# cd ""C:\Users\eduar\source\repos\Abbott-New"
#.\.venv\Scripts\Activate.ps1

import os
import yfinance as yf
import pandas as pd
from pathlib import Path

def get_downloads_folder() -> str:
    """
    Return the user’s Downloads folder path in a cross-platform way.
    """
    home = Path.home()
    # On Windows this may not always work if Downloads folder is relocated,
    # but this covers most default setups. :contentReference[oaicite:0]{index=0}
    return str(home / "Downloads")

def download_daily_data(ticker: str, start_date: str, end_date: str, filename: str = None):
    """
    Download daily historical data for the given ticker between start_date and end_date,
    then export the result to CSV in the Downloads folder (unless filename includes full path).
    """
    # Prepare output path
    downloads_folder = get_downloads_folder()
    if filename is None:
        filename = f"{ticker}_daily.csv"
    output_path = os.path.join(downloads_folder, filename)

    # Create ticker object
    stock = yf.Ticker(ticker)
    # Download history with daily interval
    df = stock.history(start=start_date, end=end_date, interval="1d", auto_adjust=True)
    # Select only the Close column and reset index
    df = df[['Close']].reset_index()
    # Rename columns for clarity
    df.columns = ['Date', 'Close']
    # Calculate daily percentage change
    df['Pct_Change'] = df['Close'].pct_change() * 100
    # Export to CSV
    df.to_csv(output_path, index=False)
    print(f"File saved to: {output_path} (rows: {len(df)})")

if __name__ == "__main__":
    download_daily_data(
        ticker="ABT",
        start_date="2015-01-01",
        end_date="2025-11-07"
    )
