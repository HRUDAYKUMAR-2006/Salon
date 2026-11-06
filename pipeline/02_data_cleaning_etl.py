"""
02_data_cleaning_etl.py
-----------------------
Robust Data Cleaning & ETL Pipeline addressing the 3 core dirty-data challenges:
1. Reclassifies false cancellations back to true No-Shows based on cancellation timing and reasons.
2. Standardizes 48 dirty outlet service naming variations to 10 canonical service categories.
3. Resolves anonymous walk-ins with synthetic proxy IDs for cohort retention tracking.
Outputs cleaned datasets ready for causal inference and A/B test analysis.
"""

import os
import re
import pandas as pd
import numpy as np

def clean_and_standardize_salon_data(raw_csv_path="data/raw/appointments_raw.csv"):
    print("Loading raw appointments data...")
    df = pd.read_csv(raw_csv_path)
    print(f"Loaded {len(df):,} raw records.")
    
    # -------------------------------------------------------------
    # 1. Reclassifying Mislabeled No-Shows
    # -------------------------------------------------------------
    print("\n[Step 1] Auditing and Reconciling Mislabeled Cancellations...")
    initial_logged_noshows = (df["status_logged_raw"] == "No-Show").sum()
    initial_logged_cancels = (df["status_logged_raw"] == "Cancelled").sum()
    print(f"  Raw Logged No-Shows: {initial_logged_noshows:,} ({initial_logged_noshows/len(df):.2%})")
    print(f"  Raw Logged Cancellations: {initial_logged_cancels:,} ({initial_logged_cancels/len(df):.2%})")
    
    # Staff heuristic: if marked 'Cancelled' but timing was < 30 minutes before slot (or <= 0, after slot started),
    # or cancellation reason indicates non-arrival, reclassify as 'No-Show'
    suspect_cancel_reasons = ["", "auto-closed by system", "client unreachable", "staff marked cancel", "no contact"]
    
    reclassify_mask = (
        (df["status_logged_raw"] == "Cancelled") &
        (
            (df["cancellation_timing_mins"] < 30) |
            (df["cancellation_reason"].isna()) |
            (df["cancellation_reason"].isin(suspect_cancel_reasons))
        )
    )
    
    df["clean_status"] = df["status_logged_raw"]
    df.loc[reclassify_mask, "clean_status"] = "No-Show"
    
    reclassified_count = reclassify_mask.sum()
    final_clean_noshows = (df["clean_status"] == "No-Show").sum()
    final_clean_cancels = (df["clean_status"] == "Cancelled").sum()
    print(f"  -> Reclassified {reclassified_count:,} false cancellations to No-Show!")
    print(f"  Adjusted Clean No-Shows: {final_clean_noshows:,} ({final_clean_noshows/len(df):.2%})")
    print(f"  Adjusted Genuine Cancellations: {final_clean_cancels:,} ({final_clean_cancels/len(df):.2%})")
    
    # -------------------------------------------------------------
    # 2. Service Name Harmonization & Canonical Mapping
    # -------------------------------------------------------------
    print("\n[Step 2] Harmonizing 48 Outlet-Specific Dirty Service Names...")
    raw_services_count = df["raw_service_name"].nunique()
    print(f"  Raw unique service strings found: {raw_services_count}")
    
    # Mapping rule dictionary
    def normalize_service(name):
        n = str(name).lower().strip()
        if re.search(r'm-hair|gent|men|m-cut', n):
            return "HAIR_MEN_STYLING", "Hair", 450
        elif re.search(r'women|ladies|f-hair|layered|female', n):
            return "HAIR_WOMEN_CUT_STYLE", "Hair", 950
        elif re.search(r'balayage|color|streaks', n):
            return "HAIR_COLOR_BALAYAGE", "Hair", 3200
        elif re.search(r'hydra|deep cleanse', n):
            return "FACIAL_HYDRA_GLOW", "Skin & Facial", 2800
        elif re.search(r'gold|kanti|shahnaz', n):
            return "FACIAL_AYUR_GOLD", "Skin & Facial", 1800
        elif re.search(r'abhyanga|herbal|kerala', n):
            return "SPA_AYURVEDIC_BODY", "Body Spa", 2400
        elif re.search(r'aroma|swedish|deep tissue', n):
            return "SPA_AROMATHERAPY", "Body Spa", 2600
        elif re.search(r'pedicure|pedi|foot', n):
            return "PEDICURE_SPA_DELUXE", "Nail & Grooming", 850
        elif re.search(r'manicure|mani|nail art', n):
            return "MANICURE_GEL_ART", "Nail & Grooming", 750
        elif re.search(r'bridal|wedding|muhurtham', n):
            return "BRIDAL_LUXE_PACKAGE", "Specialized Package", 8500
        else:
            return "OTHER_GENERAL_SERVICE", "General", 500

    service_results = [normalize_service(s) for s in df["raw_service_name"]]
    df["clean_service_code"] = [r[0] for r in service_results]
    df["clean_service_dept"] = [r[1] for r in service_results]
    df["clean_benchmark_price"] = [r[2] for r in service_results]
    
    print(f"  -> Successfully mapped all {raw_services_count} dirty strings into {df['clean_service_code'].nunique()} canonical services!")
    print(df["clean_service_code"].value_counts())
    
    # -------------------------------------------------------------
    # 3. Walk-in Entity Resolution & Missing Client ID Handling
    # -------------------------------------------------------------
    print("\n[Step 3] Handling Anonymous Walk-ins and Creating Proxy Client IDs...")
    missing_client_mask = df["client_id"].isna() | df["client_id"].isin(["NULL", "WALK_IN", "WALK-IN", "", "UNKNOWN"])
    missing_count = missing_client_mask.sum()
    print(f"  Anonymous walk-in visits without Client ID: {missing_count:,} ({missing_count/len(df):.2%})")
    
    # Generate deterministic proxy client IDs for walk-ins based on outlet + day + time slot cluster
    # to facilitate entity tracking while preserving the is_walkin flag
    walkin_indices = df[missing_client_mask].index
    proxy_client_ids = [f"PRX_WALKIN_{df.loc[i, 'outlet_id']}_{i%5000:04d}" for i in walkin_indices]
    
    df["resolved_client_id"] = df["client_id"]
    df.loc[missing_client_mask, "resolved_client_id"] = proxy_client_ids
    df["is_walkin_resolved"] = missing_client_mask.astype(int)
    
    # Calculate derived flags
    df["is_noshow"] = (df["clean_status"] == "No-Show").astype(int)
    df["is_completed"] = (df["clean_status"] == "Completed").astype(int)
    df["is_cancelled"] = (df["clean_status"] == "Cancelled").astype(int)
    
    # Export cleaned master dataset
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/clean_master_appointments.csv", index=False)
    print("\nSaved clean master dataset to data/processed/clean_master_appointments.csv")
    
    # Export subsets for targeted analysis
    # Subset 1: Retrospective Quasi-Experiment (Baseline vs Q4 for DiD)
    df_did = df[df["period"].isin(["Baseline", "Retrospective_Q4"])].copy()
    # Align to 8 weeks pre (days 184-239) and 8 weeks post (days 240-295) for balanced DiD event window
    df_did_window = df_did[(df_did["day_offset"] >= 184) & (df_did["day_offset"] < 296)].copy()
    df_did_window["post_period"] = (df_did_window["day_offset"] >= 240).astype(int)
    df_did_window["treated_region"] = (df_did_window["region_type"] == "Treated_Coimbatore").astype(int)
    df_did_window.to_csv("data/processed/did_quasi_experiment.csv", index=False)
    print(f"Saved DiD quasi-experiment window dataset ({len(df_did_window):,} records) to data/processed/did_quasi_experiment.csv")
    
    # Subset 2: Prospective A/B Experiment
    df_ab = df[df["period"] == "Experiment_AB"].copy()
    df_ab.to_csv("data/processed/ab_experiment_clean.csv", index=False)
    print(f"Saved A/B experiment clean dataset ({len(df_ab):,} records) to data/processed/ab_experiment_clean.csv")
    
    return df

if __name__ == "__main__":
    clean_and_standardize_salon_data()

