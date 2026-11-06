"""
01_generate_salon_dataset.py
----------------------------
Generates a realistic 300,000-record salon & spa dataset for Kongu Luxe Salon & Spa Chain
operating across 22 outlets in Coimbatore (18 outlets) and Western Tamil Nadu control region
(4 outlets in Tiruppur and Erode).

Includes real-world messy data nuances:
1. No-shows misclassified as cancellations
2. Service names that differ by outlet (48 dirty naming variations)
3. Walk-ins recorded without client IDs
4. Multi-period timeline:
   - Historical Baseline (Months 1-8)
   - Retrospective Business Change Period (Months 9-12): Management change in Coimbatore outlets
     with festive seasonality (Navaratri, Diwali, Muhurtham wedding dates) vs Control region.
   - Prospective A/B Experiment Period (Month 13-14): 1:1 Randomized Trial for Smart Dynamic Reminders.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_salon_data(n_records=300000, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    
    print(f"Generating {n_records:,} raw records for Kongu Luxe Salon & Spa Chain...")
    
    # 1. Outlets Metadata
    outlets = [
        # Coimbatore Urban / Prime Malls
        {"id": "OUT_01", "name": "Brookefields Mall", "city": "Coimbatore", "cluster": "Prime Mall", "tier": "A", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_02", "name": "Prozone Mall", "city": "Coimbatore", "cluster": "Prime Mall", "tier": "A", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_03", "name": "Race Course Road", "city": "Coimbatore", "cluster": "Prime Mall", "tier": "A", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_04", "name": "RS Puram North", "city": "Coimbatore", "cluster": "Prime Mall", "tier": "A", "region_type": "Treated_Coimbatore"},
        # Coimbatore High-Street Commercial
        {"id": "OUT_05", "name": "RS Puram - DB Road", "city": "Coimbatore", "cluster": "High Street", "tier": "A", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_06", "name": "Gandhipuram - Cross Cut", "city": "Coimbatore", "cluster": "High Street", "tier": "B", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_07", "name": "Gandhipuram Central", "city": "Coimbatore", "cluster": "High Street", "tier": "B", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_08", "name": "Saibaba Colony", "city": "Coimbatore", "cluster": "High Street", "tier": "B", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_09", "name": "Peelamedu - Avinashi Rd", "city": "Coimbatore", "cluster": "High Street", "tier": "B", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_10", "name": "Ramanathapuram", "city": "Coimbatore", "cluster": "High Street", "tier": "B", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_11", "name": "Singanallur", "city": "Coimbatore", "cluster": "High Street", "tier": "C", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_12", "name": "Ganapathy", "city": "Coimbatore", "cluster": "High Street", "tier": "C", "region_type": "Treated_Coimbatore"},
        # Coimbatore Suburban & Tech Corridors
        {"id": "OUT_13", "name": "Saravanampatti IT Park", "city": "Coimbatore", "cluster": "Suburban", "tier": "B", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_14", "name": "Vadavalli", "city": "Coimbatore", "cluster": "Suburban", "tier": "C", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_15", "name": "Thudiyalur", "city": "Coimbatore", "cluster": "Suburban", "tier": "C", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_16", "name": "Kuniyamuthur", "city": "Coimbatore", "cluster": "Suburban", "tier": "C", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_17", "name": "Kovaipudur", "city": "Coimbatore", "cluster": "Suburban", "tier": "C", "region_type": "Treated_Coimbatore"},
        {"id": "OUT_18", "name": "Sulur", "city": "Coimbatore", "cluster": "Suburban", "tier": "C", "region_type": "Treated_Coimbatore"},
        # Western Tamil Nadu Control Outlets (Tiruppur & Erode)
        {"id": "OUT_19", "name": "Tiruppur - Town Hall", "city": "Tiruppur", "cluster": "High Street", "tier": "B", "region_type": "Control_WesternTN"},
        {"id": "OUT_20", "name": "Tiruppur - Avinashi Rd", "city": "Tiruppur", "cluster": "High Street", "tier": "B", "region_type": "Control_WesternTN"},
        {"id": "OUT_21", "name": "Erode - Brough Road", "city": "Erode", "cluster": "High Street", "tier": "B", "region_type": "Control_WesternTN"},
        {"id": "OUT_22", "name": "Erode - Perundurai Rd", "city": "Erode", "cluster": "Suburban", "tier": "C", "region_type": "Control_WesternTN"},
    ]
    df_outlets = pd.DataFrame(outlets)
    df_outlets.to_csv("data/raw/outlets_metadata.csv", index=False)
    
    # 2. Canonical Services & Outlet-Specific Dirty Variations
    canonical_services = {
        "HAIR_MEN_STYLING": {
            "dept": "Hair", "base_price": 450, "duration": 30,
            "variations": ["M-Haircut Classic", "Gent's Hair Cut", "Men Stylist Cut", "Haircut Men Classic", "MENS HAIRSTYLE"]
        },
        "HAIR_WOMEN_CUT_STYLE": {
            "dept": "Hair", "base_price": 950, "duration": 50,
            "variations": ["Women Haircut & Blowdry", "F-Hair Styling Deluxe", "Ladies Cut & Wash", "Women Layered Cut", "Female Hair Cut"]
        },
        "HAIR_COLOR_BALAYAGE": {
            "dept": "Hair", "base_price": 3200, "duration": 120,
            "variations": ["Balayage Highlights", "Global Hair Color & Streaks", "Balayage Color Spec", "Hair Color - Balayage Luxe"]
        },
        "FACIAL_HYDRA_GLOW": {
            "dept": "Skin & Facial", "base_price": 2800, "duration": 60,
            "variations": ["HydraFacial Glow", "Hydra Facial 60m", "Hydra-Facial Pro", "Hydration Glow Facial", "Hydra Deep Cleanse"]
        },
        "FACIAL_AYUR_GOLD": {
            "dept": "Skin & Facial", "base_price": 1800, "duration": 50,
            "variations": ["Gold Glow Facial", "Ayurvedic Gold Kanti Facial", "Ayur Herbal Gold", "Shahnaz Gold Facial"]
        },
        "SPA_AYURVEDIC_BODY": {
            "dept": "Body Spa", "base_price": 2400, "duration": 60,
            "variations": ["Ayur Herbal Abhyanga Spa", "Ayurvedic Body Massage", "Full Body Spa - Herbal", "Ayur Spa Ritual", "Kerala Abhyanga Spa"]
        },
        "SPA_AROMATHERAPY": {
            "dept": "Body Spa", "base_price": 2600, "duration": 60,
            "variations": ["Aromatherapy Body Massage", "Aroma Bliss Spa", "Deep Tissue Aromatherapy", "Swedish Aroma Spa"]
        },
        "PEDICURE_SPA_DELUXE": {
            "dept": "Nail & Grooming", "base_price": 850, "duration": 40,
            "variations": ["Organic Aloe Pedicure", "Spa Pedi Deluxe", "Foot Reflexology Pedicure", "Pedicure - Spa Organic", "Deluxe Foot Spa"]
        },
        "MANICURE_GEL_ART": {
            "dept": "Nail & Grooming", "base_price": 750, "duration": 35,
            "variations": ["Gel Manicure & Polish", "Nail Art & French Mani", "Spa Manicure Express", "Deluxe Mani Polish"]
        },
        "BRIDAL_LUXE_PACKAGE": {
            "dept": "Specialized Package", "base_price": 8500, "duration": 180,
            "variations": ["Bridal Muhurtham Glow", "Bridal Makeup & Hair", "Wedding Bride Luxe Package", "Pre-Bridal Glow Ritual"]
        }
    }
    
    # 3. Stylists
    stylists = []
    seniority_levels = ["Junior", "Senior", "Master Stylist"]
    for i in range(1, 121):
        stylists.append({
            "stylist_id": f"STY_{i:03d}",
            "name": f"Stylist {i}",
            "seniority": np.random.choice(seniority_levels, p=[0.45, 0.40, 0.15]),
            "base_rating": round(np.random.uniform(4.2, 4.9), 2)
        })
    df_stylists = pd.DataFrame(stylists)
    df_stylists.to_csv("data/raw/stylists.csv", index=False)
    
    # 4. Generate Timeline & Appointments
    # Timeline: 420 days total (Jan 2025 - Feb 2026)
    # Day 1 - 240: Pre-intervention baseline (Months 1-8)
    # Day 241 - 360: Retrospective change period (Months 9-12 / Q4: Diwali, wedding season)
    # Day 361 - 420: Prospective A/B Experiment period (Months 13-14)
    start_date = datetime(2025, 1, 1)
    
    # Generate random days
    day_offsets = np.random.randint(0, 420, size=n_records)
    # Give higher density to weekend and festive season (days 270-330 = Oct-Nov Diwali season)
    # Re-sample days with realistic seasonality weights
    day_weights = np.ones(420)
    # Day-of-week pattern (cycle of 7)
    for d in range(420):
        dow = (start_date + timedelta(days=d)).weekday()
        if dow in [5, 6]: # Sat, Sun
            day_weights[d] *= 1.45
        elif dow == 4: # Friday
            day_weights[d] *= 1.15
        # Festive Season (Day 270 - 325 corresponds to Oct-Nov Diwali & Muhurtham wedding surge)
        if 270 <= d <= 325:
            day_weights[d] *= 1.35
        # Post-festive lull (Jan days 365-385)
        if 365 <= d <= 385:
            day_weights[d] *= 0.90
            
    day_weights /= day_weights.sum()
    appointment_days = np.random.choice(np.arange(420), size=n_records, p=day_weights)
    appointment_dates = [start_date + timedelta(days=int(d)) for d in appointment_days]
    
    # Outlet assignments: Weighted by outlet size
    outlet_weights = np.array([
        0.07, 0.065, 0.06, 0.06, # 4 Prime Malls (25.5%)
        0.05, 0.055, 0.05, 0.045, 0.045, 0.045, 0.04, 0.04, # 8 High Street (37%)
        0.045, 0.04, 0.035, 0.035, 0.03, 0.03, # 6 Suburban (21.5%)
        0.045, 0.04, 0.04, 0.035 # 4 Control Western TN (16%)
    ])
    outlet_weights /= outlet_weights.sum()
    chosen_outlets_idx = np.random.choice(len(outlets), size=n_records, p=outlet_weights)
    
    # Service selection
    service_keys = list(canonical_services.keys())
    service_probs = [0.24, 0.20, 0.08, 0.12, 0.09, 0.08, 0.06, 0.06, 0.05, 0.02]
    chosen_service_idx = np.random.choice(len(service_keys), size=n_records, p=service_probs)
    
    # Client ID generation: 60,000 unique known clients + anonymous walk-ins
    n_known_clients = 60000
    known_client_pool = [f"CLT_{i:06d}" for i in range(1, n_known_clients + 1)]
    # Pareto principle: 20% of clients generate 60% of bookings
    client_weights = np.random.pareto(a=1.5, size=n_known_clients)
    client_weights /= client_weights.sum()
    
    # 22% of bookings are spontaneous walk-ins without client IDs!
    is_walkin = np.random.rand(n_records) < 0.22
    client_ids = []
    
    random_client_sample = np.random.choice(known_client_pool, size=n_records, p=client_weights)
    for idx, walkin in enumerate(is_walkin):
        if walkin:
            # Messy logging: NULL, 'WALK_IN', or blank
            missing_variant = np.random.choice(["NULL", "WALK_IN", "WALK-IN", "", "UNKNOWN"])
            client_ids.append(missing_variant)
        else:
            client_ids.append(random_client_sample[idx])
            
    # Stylists assignment
    stylist_ids = np.random.choice(df_stylists["stylist_id"].values, size=n_records)
    
    # Build dataframe pieces
    chosen_outlet_data = [outlets[i] for i in chosen_outlets_idx]
    outlet_id = [o["id"] for o in chosen_outlet_data]
    outlet_name = [o["name"] for o in chosen_outlet_data]
    outlet_city = [o["city"] for o in chosen_outlet_data]
    outlet_cluster = [o["cluster"] for o in chosen_outlet_data]
    outlet_tier = [o["tier"] for o in chosen_outlet_data]
    region_type = [o["region_type"] for o in chosen_outlet_data]
    
    # Generate dirty service names
    raw_service_names = []
    service_base_prices = []
    service_canonical_keys = []
    service_durations = []
    service_depts = []
    
    for idx in chosen_service_idx:
        key = service_keys[idx]
        srv = canonical_services[key]
        service_canonical_keys.append(key)
        service_base_prices.append(srv["base_price"])
        service_durations.append(srv["duration"])
        service_depts.append(srv["dept"])
        # Dirty variation picked at random
        raw_service_names.append(random.choice(srv["variations"]))
        
    df = pd.DataFrame({
        "appointment_id": [f"APT_{i+1000000}" for i in range(n_records)],
        "appointment_date": [d.strftime("%Y-%m-%d") for d in appointment_dates],
        "appointment_time": [f"{random.randint(9, 20):02d}:{random.choice(['00', '15', '30', '45'])}" for _ in range(n_records)],
        "day_offset": appointment_days,
        "outlet_id": outlet_id,
        "outlet_name": outlet_name,
        "outlet_city": outlet_city,
        "outlet_cluster": outlet_cluster,
        "outlet_tier": outlet_tier,
        "region_type": region_type,
        "client_id": client_ids,
        "is_walkin": is_walkin.astype(int),
        "stylist_id": stylist_ids,
        "raw_service_name": raw_service_names,
        "service_canonical": service_canonical_keys,
        "service_department": service_depts,
        "base_service_price": service_base_prices,
        "service_duration": service_durations
    })
    
    # 5. Define Periods:
    # Baseline: day < 240
    # Retrospective Period (DiD): 240 <= day < 360 (Treated = Coimbatore, Control = Western TN)
    # Prospective Experiment Period (A/B Test): day >= 360
    df["period"] = "Baseline"
    df.loc[(df["day_offset"] >= 240) & (df["day_offset"] < 360), "period"] = "Retrospective_Q4"
    df.loc[df["day_offset"] >= 360, "period"] = "Experiment_AB"
    
    # A/B Experiment Assignment (for day >= 360)
    # 1:1 user-level or appointment-level randomization
    df["ab_variant"] = "None"
    ab_mask = df["period"] == "Experiment_AB"
    # Random assignment with 50/50 probability
    ab_alloc = np.random.choice(["Control", "Treatment"], size=ab_mask.sum(), p=[0.50, 0.50])
    df.loc[ab_mask, "ab_variant"] = ab_alloc
    
    # 6. Simulate Status and Outcomes:
    # Status options: 'Completed', 'Cancelled', 'No-Show'
    # Real-world dirty nuance: front-desk frequently marks No-Shows as Cancelled!
    # Base no-show rate ~18.5%, cancellation rate ~8%, completion rate ~73.5%
    
    # Base probabilities
    prob_completed = np.full(n_records, 0.735)
    prob_noshow = np.full(n_records, 0.185)
    prob_cancelled = np.full(n_records, 0.080)
    
    # Tier effect: Tier A has lower no-shows (15%), Tier C has higher (22%)
    prob_noshow[df["outlet_tier"] == "A"] -= 0.035
    prob_noshow[df["outlet_tier"] == "C"] += 0.035
    
    # Weekend effect: higher no-show on weekends (traffic, plan changes)
    dow_arr = np.array([d.weekday() for d in appointment_dates])
    weekend_mask = (dow_arr >= 5)
    prob_noshow[weekend_mask] += 0.025
    
    # Walk-in effect: Walk-ins are present right then, so completed probability is higher, no-show is 0 for immediate walk-ins
    # But walk-in pre-bookings (same day waiting) have 5% no-show
    prob_noshow[is_walkin] = 0.04
    prob_completed[is_walkin] = 0.94
    prob_cancelled[is_walkin] = 0.02
    
    # Prospective A/B Test Treatment Effect:
    # Treatment is "Smart WhatsApp Interactive Confirmation + Micro-Deposit Protocol"
    # Reduces no-show by -4.3% absolute!
    treat_ab_mask = (df["period"] == "Experiment_AB") & (df["ab_variant"] == "Treatment")
    prob_noshow[treat_ab_mask] -= 0.043
    prob_completed[treat_ab_mask] += 0.038
    prob_cancelled[treat_ab_mask] += 0.005 # slight cancellation notice instead of ghosting
    
    # Normalize probabilities
    total_p = prob_completed + prob_noshow + prob_cancelled
    prob_completed /= total_p
    prob_noshow /= total_p
    prob_cancelled /= total_p
    
    # Draw true status
    rand_status = np.random.rand(n_records)
    true_status = np.where(rand_status < prob_completed, "Completed",
                  np.where(rand_status < prob_completed + prob_noshow, "No-Show", "Cancelled"))
    df["true_status"] = true_status
    
    # NOW: Introduce the dirty logging bias!
    # In raw records, 42% of actual No-Shows are logged by receptionists as "Cancelled"!
    raw_status = true_status.copy()
    cancellation_timing_mins = np.full(n_records, np.nan) # minutes before/after slot
    cancellation_reason = np.full(n_records, "", dtype=object)
    
    # For genuine cancellations: cancelled 120 - 2880 mins (2h to 48h) before slot
    gen_cancel_mask = (true_status == "Cancelled")
    cancellation_timing_mins[gen_cancel_mask] = np.random.randint(120, 2880, size=gen_cancel_mask.sum())
    cancellation_reason[gen_cancel_mask] = np.random.choice(
        ["Client Schedule Conflict", "Illness / Personal Emergency", "Travel / Out of Station", "Rescheduled to next week"],
        size=gen_cancel_mask.sum()
    )
    
    # For No-Shows:
    noshow_mask = (true_status == "No-Show")
    # 42% mislabeled as Cancelled!
    mislabeled_mask = noshow_mask & (np.random.rand(n_records) < 0.42)
    raw_status[mislabeled_mask] = "Cancelled"
    
    # Timing for mislabeled no-shows: staff marked Cancelled after appointment time or < 15 mins before
    cancellation_timing_mins[mislabeled_mask] = np.random.randint(-180, 15, size=mislabeled_mask.sum())
    cancellation_reason[mislabeled_mask] = np.random.choice(
        ["", "auto-closed by system", "client unreachable", "staff marked cancel", "no contact"],
        p=[0.40, 0.25, 0.15, 0.10, 0.10],
        size=mislabeled_mask.sum()
    )
    
    df["status_logged_raw"] = raw_status
    df["cancellation_timing_mins"] = cancellation_timing_mins
    df["cancellation_reason"] = cancellation_reason
    
    # 7. Revenue Simulation (Service price + Product Add-on sales + Tip)
    # Retrospective business change (DiD):
    # Base revenue per completed visit ~ ₹1,420
    # During Q4 (day 240-360):
    # - Seasonality (festive / Diwali / Muhurtham) lifts spending in ALL outlets (Coimbatore + Control) by ~ +₹162 (+11.4%)
    # - Retrospective Change in Coimbatore (upselling bundle protocol) adds an ADDITIONAL true causal lift of +₹103 (+7.2%)
    # Total observed lift in Coimbatore: ₹162 (seasonal) + ₹103 (treatment) = +₹265 (+18.6%)!
    
    completed_mask = (df["true_status"] == "Completed")
    
    # Product sales cross-sell: 25% base attachment rate, average ₹450
    prod_attachment_prob = np.full(n_records, 0.24)
    # Tier A has higher product retail attachment
    prod_attachment_prob[df["outlet_tier"] == "A"] += 0.08
    
    # Festive season has higher retail purchase (gifting, festivals)
    festive_mask = (df["day_offset"] >= 270) & (df["day_offset"] <= 330)
    prod_attachment_prob[festive_mask] += 0.10
    
    # Retrospective change in Coimbatore boosted product cross-sell & service add-ons!
    retro_treated_mask = (df["period"] == "Retrospective_Q4") & (df["region_type"] == "Treated_Coimbatore")
    prod_attachment_prob[retro_treated_mask] += 0.09
    
    has_product_sale = completed_mask & (np.random.rand(n_records) < prod_attachment_prob)
    product_sales = np.where(has_product_sale, np.random.exponential(scale=380, size=n_records) + 150, 0.0)
    product_sales = np.round(product_sales, 0)
    
    # Service price with slight variations/promotions
    service_price_paid = np.array(service_base_prices, dtype=float)
    # In treated retrospective period, Coimbatore outlets had package add-on (+7% on service ticket)
    service_price_paid[retro_treated_mask & completed_mask] *= np.random.uniform(1.05, 1.10, size=(retro_treated_mask & completed_mask).sum())
    # Festive general uplift (+8% across all outlets in Oct-Nov)
    service_price_paid[festive_mask & completed_mask] *= np.random.uniform(1.04, 1.11, size=(festive_mask & completed_mask).sum())
    
    service_price_paid = np.round(service_price_paid, 0)
    # If not completed, revenue is 0
    service_price_paid[~completed_mask] = 0.0
    product_sales[~completed_mask] = 0.0
    
    # Tip amount
    tip_amount = np.where(completed_mask, np.random.choice([0, 50, 100, 200], p=[0.55, 0.25, 0.15, 0.05], size=n_records), 0.0)
    
    df["service_revenue"] = service_price_paid
    df["product_revenue"] = product_sales
    df["tip_amount"] = tip_amount
    df["total_revenue"] = service_price_paid + product_sales
    
    # Pre-experiment historical 90-day spend covariate for CUPED (repeat client prior spend)
    # Strong correlation with current visit spend (rho ~ 0.62)
    # Synthetic baseline spend generated from client true latent spending affinity
    client_latent_affinity = np.random.lognormal(mean=7.2, sigma=0.45, size=n_known_clients)
    client_affinity_map = dict(zip(known_client_pool, client_latent_affinity))
    
    # Map to dataframe
    base_prior_spend = np.array([client_affinity_map.get(cid, 0.0) if cid in client_affinity_map else 0.0 for cid in df["client_id"]])
    # Add noise
    prior_spend_covariate = np.where(
        base_prior_spend > 0,
        np.maximum(0, 0.70 * base_prior_spend + 0.30 * df["total_revenue"] + np.random.normal(0, 350, size=n_records)),
        0.0
    )
    df["pre_exp_historical_spend"] = np.round(prior_spend_covariate, 0)
    
    # Customer Satisfaction Rating (CSAT 1-5, for completed visits)
    csat = np.full(n_records, np.nan)
    csat_scores = np.random.choice([1, 2, 3, 4, 5], p=[0.02, 0.03, 0.08, 0.32, 0.55], size=completed_mask.sum())
    csat[completed_mask] = csat_scores
    df["csat_rating"] = csat
    
    print(f"Dataset generated successfully with {len(df):,} records!")
    print(f"Summary by period:")
    print(df["period"].value_counts())
    print("\nSummary by region type:")
    print(df["region_type"].value_counts())
    print("\nRaw logged status vs True status:")
    print(pd.crosstab(df["status_logged_raw"], df["true_status"]))
    
    # Save raw datasets
    df.to_csv("data/raw/appointments_raw.csv", index=False)
    print("Saved data/raw/appointments_raw.csv")
    
    return df

if __name__ == "__main__":
    generate_salon_data(n_records=300000, seed=42)

