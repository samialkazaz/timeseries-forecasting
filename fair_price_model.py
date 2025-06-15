import sys
import json
import requests
import pandas as pd
import yfinance as yf

"""Simple stock fair price estimator.

This script downloads recent price data and limited fundamental metrics for a
specified ticker. It then performs a naive fair value estimate based on the
historical average price-to-earnings (P/E) ratio. This example is highly
simplified and meant for educational purposes only.

USAGE:
    python fair_price_model.py AAPL

Note: This script relies on third-party APIs that may require an internet
connection and is provided without warranty. It does not constitute financial
advice.
"""

def fetch_financials(ticker: str) -> dict:
    """Fetch basic financial metrics from Yahoo Finance via yfinance."""
    stock = yf.Ticker(ticker)
    info = stock.get_info()
    # Extract a few fields; many others are available
    return {
        "currentPrice": info.get("currentPrice"),
        "trailingPE": info.get("trailingPE"),
        "epsTrailingTwelveMonths": info.get("trailingEps"),
    }


def estimate_fair_price(financials: dict) -> float:
    """Naively compute a fair price from trailing EPS and historical P/E."""
    eps = financials.get("epsTrailingTwelveMonths")
    pe = financials.get("trailingPE")
    if eps is None or pe is None:
        raise ValueError("Missing EPS or P/E data for fair price estimate")
    return eps * pe


def main(ticker: str) -> None:
    print(f"Fetching data for {ticker}...")
    financials = fetch_financials(ticker)
    print(json.dumps(financials, indent=2))

    try:
        fair_price = estimate_fair_price(financials)
    except ValueError as exc:
        print("Could not compute fair price:", exc)
        return

    print(f"Estimated fair price for {ticker}: ${fair_price:.2f}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fair_price_model.py TICKER")
    else:
        main(sys.argv[1].upper())
