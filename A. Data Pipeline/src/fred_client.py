"""
FRED API Client
===============
Fetch macroeconomic time series from the Federal Reserve (FRED).
Requires a free API key: https://fred.stlouisfed.org/docs/api/api_key.html
"""

import time

import pandas as pd
import requests

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

# Default series for credit risk analysis
DEFAULT_SERIES = {
    "FEDFUNDS": "Federal Funds Rate",
    "MORTGAGE30US": "30-Year Fixed Mortgage Rate",
    "DGS10": "10-Year Treasury Rate",
    "T10Y2Y": "10Y-2Y Yield Spread",
    "UNRATE": "Unemployment Rate",
    "CPIAUCSL": "Consumer Price Index",
    "DRALACBS": "Delinquency Rate All Loans",
    "DRSFRMACBN": "Delinquency Rate Mortgage SFR",
    "GDP": "Gross Domestic Product",
    "CSUSHPINSA": "Case-Shiller Home Price Index",
}


def scrape_fred_series(
    series_id: str,
    api_key: str,
    start_date: str = "2019-01-01",
) -> pd.DataFrame:
    """
    Fetch a single FRED series.

    Parameters
    ----------
    series_id : str
        FRED series ID, e.g. "FEDFUNDS".
    api_key : str
        Your FRED API key.
    start_date : str
        Start date in YYYY-MM-DD format.

    Returns
    -------
    pd.DataFrame
        Two-column DataFrame: date, <series_id>.
    """
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date,
    }

    response = requests.get(FRED_BASE, params=params)
    response.raise_for_status()

    observations = response.json()["observations"]
    df = pd.DataFrame(observations)[["date", "value"]]
    df.columns = ["date", series_id.lower()]
    df["date"] = pd.to_datetime(df["date"])
    df[series_id.lower()] = pd.to_numeric(df[series_id.lower()], errors="coerce")
    return df


def scrape_all_fred(
    api_key: str,
    series_dict: dict | None = None,
    start_date: str = "2019-01-01",
    sleep_seconds: float = 0.3,
) -> pd.DataFrame:
    """
    Fetch multiple FRED series and merge into one DataFrame.

    Parameters
    ----------
    api_key : str
        Your FRED API key.
    series_dict : dict or None
        {series_id: description}. Uses DEFAULT_SERIES if None.
    start_date : str
        Start date for all series.
    sleep_seconds : float
        Delay between API calls.

    Returns
    -------
    pd.DataFrame
        Merged DataFrame with all series, indexed by date.
    """
    if series_dict is None:
        series_dict = DEFAULT_SERIES

    frames = {}
    for sid, name in series_dict.items():
        print(f"[SCRAPING] {sid} — {name}")
        try:
            df_s = scrape_fred_series(sid, api_key, start_date)
            frames[sid] = df_s
            print(f"  → {len(df_s)} observations")
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
        time.sleep(sleep_seconds)

    if not frames:
        raise RuntimeError("No FRED series were successfully fetched.")

    # Merge all series on date
    series_ids = list(frames.keys())
    df_merged = frames[series_ids[0]]
    for sid in series_ids[1:]:
        df_merged = pd.merge(df_merged, frames[sid], on="date", how="outer")

    df_merged = df_merged.sort_values("date").reset_index(drop=True)
    return df_merged
