"""
HMDA Data Browser API Scraper
=============================
Scrape loan-level mortgage data from CFPB/FFIEC.
No API key required.

API Docs: https://ffiec.cfpb.gov/documentation/api/data-browser/
"""

import os
import time

import pandas as pd
import requests

HMDA_BASE = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv"


def scrape_hmda_loans(
    states: list[str],
    years: list[int],
    actions_taken: list[int],
    output_dir: str | None = None,
    sleep_seconds: float = 1.0,
) -> pd.DataFrame:
    """
    Scrape loan-level data from the HMDA Data Browser API.

    Parameters
    ----------
    states : list[str]
        State codes, e.g. ["CA", "TX", "FL"].
    years : list[int]
        Filing years, e.g. [2022].
    actions_taken : list[int]
        Action taken codes: 1=Originated, 3=Denied.
    output_dir : str or None
        If provided, save raw CSV per year to this directory.
    sleep_seconds : float
        Delay between requests for rate limiting.

    Returns
    -------
    pd.DataFrame
        Combined DataFrame with all scraped records.
    """
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    all_frames = []

    for year in years:
        params = {
            "years": year,
            "states": ",".join(states),
            "actions_taken": ",".join(str(a) for a in actions_taken),
        }

        print(f"[SCRAPING] HMDA {year} | States: {states} | Actions: {actions_taken}")
        response = requests.get(HMDA_BASE, params=params, stream=True)
        response.raise_for_status()

        # Stream to temp file for large responses
        temp_file = os.path.join(output_dir or ".", f"hmda_{year}_temp.csv")
        with open(temp_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        df_year = pd.read_csv(temp_file, low_memory=False)
        df_year["scrape_year"] = year
        all_frames.append(df_year)
        print(f"  → {len(df_year):,} records scraped")

        # Clean up temp file if output_dir not specified
        if not output_dir and os.path.exists(temp_file):
            os.remove(temp_file)

        time.sleep(sleep_seconds)

    df_all = pd.concat(all_frames, ignore_index=True)
    return df_all


def scrape_hmda_aggregations(
    states: list[str],
    years: list[int],
    actions_taken: list[int],
) -> dict:
    """
    Fetch aggregated HMDA statistics (JSON) instead of raw CSV.

    Returns
    -------
    dict
        JSON response with aggregation counts and sums.
    """
    url = "https://ffiec.cfpb.gov/v2/data-browser-api/view/aggregations"
    params = {
        "years": ",".join(str(y) for y in years),
        "states": ",".join(states),
        "actions_taken": ",".join(str(a) for a in actions_taken),
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
