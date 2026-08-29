"""
FDIC BankFind Suite API Scraper
===============================
Scrape banking statistics and failure data from FDIC.
No API key required.

API Docs: https://banks.data.fdic.gov/docs/
"""

import pandas as pd
import requests

FDIC_API = "https://banks.data.fdic.gov/api"


def scrape_fdic_financials(
    report_date: str = "20221231",
    limit: int = 10000,
) -> pd.DataFrame:
    """
    Scrape FDIC financial data for commercial banks.

    Parameters
    ----------
    report_date : str
        Reporting date in YYYYMMDD format, e.g. "20221231".
    limit : int
        Max number of records to fetch.

    Returns
    -------
    pd.DataFrame
        Bank financial data.
    """
    url = f"{FDIC_API}/financials"
    params = {
        "filters": f"REPDTE:{report_date}",
        "fields": ",".join([
            "REPDTE", "CERT", "INSTNAME", "CITY", "STALP",
            "ASSET", "DEP", "LNLSNET",
            "P3ASSET", "P9ASSET", "NCLNLS",
            "NITEFYQ", "ROA", "ROE",
        ]),
        "limit": limit,
        "offset": 0,
        "sort_by": "ASSET",
        "sort_order": "DESC",
    }

    print(f"[SCRAPING] FDIC Financials (report date: {report_date})")
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()["data"]
    records = [item["data"] for item in data]
    df = pd.DataFrame(records)
    print(f"  → {len(df)} bank records scraped")
    return df


def scrape_fdic_failures(limit: int = 5000) -> pd.DataFrame:
    """
    Scrape list of failed banks from FDIC.

    Parameters
    ----------
    limit : int
        Max number of records to fetch.

    Returns
    -------
    pd.DataFrame
        Bank failure records with dates, costs, and resolution types.
    """
    url = f"{FDIC_API}/failures"
    params = {
        "fields": ",".join([
            "CERT", "INSTNAME", "CITY", "ST",
            "FAILDATE", "COST", "RESTYPE", "QBFASSET",
        ]),
        "limit": limit,
        "sort_by": "FAILDATE",
        "sort_order": "DESC",
    }

    print("[SCRAPING] FDIC Bank Failures")
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()["data"]
    records = [item["data"] for item in data]
    df = pd.DataFrame(records)
    print(f"  → {len(df)} failure records scraped")
    return df
