"""
Feature Engineering
===================
Functions for creating the Gold layer (Risk Feature Store).
Silver → Gold transformation.
"""

import numpy as np
import pandas as pd


def create_risk_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create risk segmentation features.

    Parameters
    ----------
    df : pd.DataFrame
        Joined loan + macro data (Silver).

    Returns
    -------
    pd.DataFrame
        DataFrame with additional risk features.
    """
    df = df.copy()

    # DTI risk bucket
    if "debt_to_income_ratio" in df.columns:
        df["dti_bucket"] = pd.cut(
            df["debt_to_income_ratio"],
            bins=[0, 20, 36, 43, 50, 200],
            labels=["Very_Low", "Low", "Moderate", "High", "Very_High"],
            include_lowest=True,
        )

    # Loan-to-Income risk bucket
    if "loan_to_income" in df.columns:
        df["lti_bucket"] = pd.cut(
            df["loan_to_income"],
            bins=[0, 2, 4, 6, 10, 1000],
            labels=["Conservative", "Standard", "Stretched", "High", "Extreme"],
            include_lowest=True,
        )

    # State-level denial rate
    if "state_code" in df.columns and "is_denied" in df.columns:
        state_rate = df.groupby("state_code")["is_denied"].mean()
        df["state_denial_rate"] = df["state_code"].map(state_rate)

    return df


def create_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create loan × macro interaction features.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with both loan and macro columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with interaction features added.
    """
    df = df.copy()

    # Rate premium over market
    if "interest_rate" in df.columns and "mortgage30us" in df.columns:
        df["rate_vs_market"] = df["interest_rate"] - df["mortgage30us"]

    # Rate × DTI interaction
    if "interest_rate" in df.columns and "debt_to_income_ratio" in df.columns:
        df["rate_x_dti"] = df["interest_rate"] * df["debt_to_income_ratio"]

    # Income × Unemployment interaction
    if "income" in df.columns and "unrate" in df.columns:
        df["income_x_unrate"] = df["income"] * df["unrate"]

    return df


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode categorical features for modeling.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with categorical columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with one-hot encoded categoricals.
    """
    df = df.copy()

    # Loan type mapping
    loan_type_map = {1: "Conventional", 2: "FHA", 3: "VA", 4: "USDA"}
    if "loan_type" in df.columns:
        df["loan_type_name"] = df["loan_type"].map(loan_type_map).fillna("Other")

    # Loan purpose mapping
    purpose_map = {
        1: "Purchase", 2: "Improvement",
        31: "Refinancing", 32: "CashOut_Refi",
        4: "Other", 5: "NA",
    }
    if "loan_purpose" in df.columns:
        df["loan_purpose_name"] = df["loan_purpose"].map(purpose_map).fillna("Other")

    # One-hot encode
    ohe_cols = [
        c for c in ["loan_type_name", "loan_purpose_name", "occupancy_type"]
        if c in df.columns
    ]
    if ohe_cols:
        df = pd.get_dummies(df, columns=ohe_cols, drop_first=True, dtype=int)

    return df


def build_gold_feature_store(
    df: pd.DataFrame,
    drop_non_modeling: bool = True,
) -> pd.DataFrame:
    """
    Full pipeline: risk features + interactions + encoding → Gold layer.

    Parameters
    ----------
    df : pd.DataFrame
        Joined Silver data (loans + macro).
    drop_non_modeling : bool
        If True, drop columns not needed for modeling.

    Returns
    -------
    pd.DataFrame
        Final risk feature store (Gold layer).
    """
    df = create_risk_features(df)
    df = create_interaction_features(df)
    df = encode_categoricals(df)

    if drop_non_modeling:
        drop_cols = [
            "lei", "county_code", "state_code",
            "denial_reason-1", "denial_reason-2", "denial_reason-3",
            "activity_year", "applicant_race-1",
            "dti_bucket", "lti_bucket",
            "loan_type", "loan_purpose",
            "derived_dwelling_category", "construction_method",
            "applicant_age", "applicant_sex",
        ]
        df = df.drop(
            columns=[c for c in drop_cols if c in df.columns],
            errors="ignore",
        )

    # Drop remaining nulls
    df = df.dropna()

    return df
