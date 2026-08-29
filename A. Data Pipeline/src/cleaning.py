"""
Data Cleaning Utilities
=======================
Functions for cleaning HMDA loan data and FRED macro data.
Bronze → Silver transformation.
"""

import numpy as np
import pandas as pd


def clean_hmda_loans(
    df: pd.DataFrame,
    missing_threshold: float = 0.6,
) -> pd.DataFrame:
    """
    Clean raw HMDA loan data (Bronze → Silver).

    Steps:
    1. Filter to Originated (1) and Denied (3) only
    2. Create binary target: is_denied
    3. Select relevant features
    4. Parse data types (handle "Exempt", text ranges)
    5. Handle missing values
    6. Basic feature engineering

    Parameters
    ----------
    df : pd.DataFrame
        Raw HMDA data from Bronze layer.
    missing_threshold : float
        Drop columns with missing rate above this threshold.

    Returns
    -------
    pd.DataFrame
        Cleaned loan data for Silver layer.
    """
    # 1. Filter & create target
    df = df[df["action_taken"].isin([1, 3])].copy()
    df["is_denied"] = (df["action_taken"] == 3).astype(int)

    # 2. Select features
    keep_cols = [
        "is_denied",
        "loan_amount", "loan_to_value_ratio",
        "interest_rate", "loan_term", "loan_type", "loan_purpose",
        "income", "debt_to_income_ratio",
        "applicant_age", "applicant_sex", "applicant_race-1",
        "derived_dwelling_category", "occupancy_type",
        "construction_method", "total_units", "property_value",
        "state_code", "county_code", "lei", "activity_year",
        "denial_reason-1", "denial_reason-2", "denial_reason-3",
    ]
    keep_cols = [c for c in keep_cols if c in df.columns]
    df = df[keep_cols].copy()

    # 3. Parse numeric columns (HMDA uses "Exempt", text ranges, etc.)
    numeric_cols = [
        "loan_amount", "income", "interest_rate", "loan_term",
        "loan_to_value_ratio", "debt_to_income_ratio", "property_value",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 4. Drop columns with too many missing values
    df = df.loc[:, df.isnull().mean() < missing_threshold]

    # 5. Fill missing values
    num_cols = df.select_dtypes(include=[np.number]).columns.drop(
        "is_denied", errors="ignore"
    )
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        df[col] = df[col].fillna("Unknown")

    # 6. Basic feature engineering
    df["loan_to_income"] = df["loan_amount"] / (
        df["income"].replace(0, np.nan) + 1
    )
    df["high_dti"] = (df["debt_to_income_ratio"] > 43).astype(int)

    return df


def clean_fred_macro(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw FRED macro data (Bronze → Silver).

    Steps:
    1. Forward-fill gaps (different series have different frequencies)
    2. Resample to monthly
    3. Create derived features (spreads, YoY changes)

    Parameters
    ----------
    df : pd.DataFrame
        Raw FRED data from Bronze layer.

    Returns
    -------
    pd.DataFrame
        Cleaned macro data for Silver layer.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").ffill()

    # Resample to month-end
    df = df.set_index("date").resample("ME").last().reset_index()

    # Derived features
    if "mortgage30us" in df.columns and "dgs10" in df.columns:
        df["mortgage_spread"] = df["mortgage30us"] - df["dgs10"]

    if "cpiaucsl" in df.columns:
        df["cpi_yoy"] = df["cpiaucsl"].pct_change(12) * 100

    if "csushpinsa" in df.columns:
        df["home_price_yoy"] = df["csushpinsa"].pct_change(12) * 100

    df["activity_year"] = df["date"].dt.year

    return df


def join_loans_macro(
    df_loans: pd.DataFrame,
    df_macro: pd.DataFrame,
) -> pd.DataFrame:
    """
    Join loan data with macro data by year.

    Parameters
    ----------
    df_loans : pd.DataFrame
        Cleaned loan data (Silver).
    df_macro : pd.DataFrame
        Cleaned macro data (Silver).

    Returns
    -------
    pd.DataFrame
        Joined dataset with macro indicators per loan.
    """
    # Aggregate macro to yearly (HMDA only has activity_year)
    macro_cols = df_macro.select_dtypes(include=[np.number]).columns.tolist()
    macro_cols = [c for c in macro_cols if c != "activity_year"]

    agg_dict = {col: "mean" for col in macro_cols}
    macro_yearly = df_macro.groupby("activity_year").agg(agg_dict).reset_index()

    df_joined = df_loans.merge(macro_yearly, on="activity_year", how="left")
    return df_joined
