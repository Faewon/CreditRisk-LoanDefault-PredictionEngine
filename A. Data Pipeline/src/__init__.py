"""
Credit Risk & Loan Default Prediction Engine
=============================================
Reusable utility modules for data scraping, cleaning, and feature engineering.
"""

from .hmda_scraper import scrape_hmda_loans
from .fred_client import scrape_fred_series, scrape_all_fred
from .fdic_scraper import scrape_fdic_financials, scrape_fdic_failures
from .cleaning import clean_hmda_loans, clean_fred_macro
from .feature_engineering import create_risk_features, create_interaction_features
