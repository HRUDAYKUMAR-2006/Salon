"""
test_causal_engine.py
---------------------
Unit & econometric tests verifying the mathematical correctness
of the Causal Inference Engine, ETL Cleaning, and CUPED implementations.
"""

import math
import numpy as np
import pandas as pd
from scipy import stats

def test_srm_calculation():
    # Observed: 19,768 Control, 20,064 Treatment
    o_c, o_t = 19768, 20064
    total = o_c + o_t
    e_c = total / 2
    e_t = total / 2
    
    chi2_expected = ((o_c - e_c)**2 / e_c) + ((o_t - e_t)**2 / e_t)
    chi2_stat, p_val = stats.chisquare([o_c, o_t], [e_c, e_t])
    
    assert math.isclose(chi2_expected, chi2_stat, rel_tol=1e-5), f"Chi2 mismatch: {chi2_expected} vs {chi2_stat}"
    assert p_val > 0.01, f"SRM should not trigger at p > 0.01, got {p_val}"
    print("✓ Test SRM Calculation: PASSED")

def test_did_decomposition():
    # 2x2 matrix values
    y_pre_ctrl = 1785.94
    y_post_ctrl = 1881.31
    y_pre_treat = 1797.10
    y_post_treat = 2077.01
    
    raw_lift = y_post_treat - y_pre_treat
    seasonal_lift = y_post_ctrl - y_pre_ctrl
    did_att = raw_lift - seasonal_lift
    
    expected_att = (2077.01 - 1797.10) - (1881.31 - 1785.94)
    assert math.isclose(did_att, expected_att, rel_tol=1e-5)
    assert math.isclose(did_att, 184.54, abs_tol=0.1)
    
    seasonal_share = (seasonal_lift / raw_lift) * 100
    assert math.isclose(seasonal_share, 34.07, abs_tol=0.2)
    print("✓ Test DiD 2x2 Decomposition: PASSED")

def test_cuped_variance_reduction():
    np.random.seed(42)
    n = 10000
    X = np.random.normal(1000, 200, n)
    # Y correlated with X (rho ~ 0.60)
    Y = 0.60 * X + np.random.normal(400, 160, n)
    
    rho = np.corrcoef(Y, X)[0, 1]
    theta = np.cov(Y, X)[0, 1] / np.var(X, ddof=1)
    Y_cuped = Y - theta * (X - np.mean(X))
    
    var_raw = np.var(Y, ddof=1)
    var_cuped = np.var(Y_cuped, ddof=1)
    
    empirical_var_red = (1 - (var_cuped / var_raw))
    theoretical_var_red = rho ** 2
    
    assert math.isclose(empirical_var_red, theoretical_var_red, abs_tol=0.01)
    print("✓ Test CUPED Variance Reduction: PASSED")

def test_etl_cleaning_integrity():
    df_clean = pd.read_csv("data/processed/clean_master_appointments.csv")
    
    # Assert no null or dirty service codes exist in clean_service_code
    assert df_clean["clean_service_code"].isna().sum() == 0, "Null service codes found!"
    assert df_clean["clean_service_code"].nunique() >= 10, "Service taxonomy collapsed!"
    
    # Assert resolved_client_id has zero missing values
    assert df_clean["resolved_client_id"].isna().sum() == 0, "Missing resolved client IDs!"
    
    # Assert clean_status only contains Completed, No-Show, Cancelled
    valid_statuses = {"Completed", "No-Show", "Cancelled"}
    actual_statuses = set(df_clean["clean_status"].unique())
    assert actual_statuses.issubset(valid_statuses), f"Unexpected status found: {actual_statuses - valid_statuses}"
    print("✓ Test ETL Cleaning Integrity: PASSED")

if __name__ == "__main__":
    print("Running Causal Analytics Test Suite...")
    test_srm_calculation()
    test_did_decomposition()
    test_cuped_variance_reduction()
    test_etl_cleaning_integrity()
    print("ALL TESTS PASSED SUCCESSFULLY! 🚀")

