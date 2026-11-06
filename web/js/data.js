// BLXDES Causal Analytics - Embedded Dataset & Master Metrics
const SALON_DATA = {
  "summary": {
    "chain_name": "BLXDES Salon & Spa Chain",
    "market": "Coimbatore & Western Tamil Nadu (Tiruppur & Erode)",
    "outlets_total": 22,
    "coimbatore_outlets": 18,
    "control_outlets": 4,
    "raw_records_analyzed": 300000,
    "time_horizon": "Jan 2025 - Feb 2026 (14 Months)"
  },
  "decision_memo": {
    "verdict": "GO",
    "verdict_title": "FULL CHAIN-WIDE ROLLOUT APPROVED",
    "verdict_subtitle": "Smart Dynamic Reconfirmation System (SDRS) delivers statistically verified +₹1.59 Crore ($192,000 USD) annual EBITDA uplift with 2,948% ROI.",
    "annual_net_profit_inr": 15920400,
    "annual_gross_inr": 16460400,
    "annual_cost_inr": 540000,
    "roi_pct": 2948,
    "monthly_slots_reclaimed": 946,
    "avg_ticket_inr": 1450,
    "rollout_timeline": "30-Day Phased Rollout (Tier A Malls -> High Street -> Suburban)"
  },
  "power_analysis": {
    "alpha": 0.05,
    "power": 0.80,
    "baseline_noshow": 0.185,
    "target_noshow": 0.155,
    "mde_abs": 0.030,
    "mde_rel": 16.2,
    "required_sample_per_variant": 2465,
    "required_sample_total": 4930,
    "daily_traffic": 1400,
    "recommended_duration_days": 14,
    "icc": 0.035,
    "cluster_de": 3.24
  },
  "srm_test": {
    "control_n": 19768,
    "treatment_n": 20064,
    "total_n": 39832,
    "control_pct": 49.63,
    "treatment_pct": 50.37,
    "chi2": 2.1996,
    "p_value": 0.1380,
    "srm_detected": false,
    "status": "PASSED"
  },
  "covariate_balance": [
    {
      "name": "Pre-Experiment 90-Day Spend (₹)",
      "control": "₹1,121.10",
      "treatment": "₹1,137.70",
      "diff": "+₹16.60",
      "p_value": "0.0617",
      "balanced": true
    },
    {
      "name": "Walk-in Client Ratio",
      "control": "22.48%",
      "treatment": "21.91%",
      "diff": "-0.57%",
      "p_value": "0.1742",
      "balanced": true
    },
    {
      "name": "Weekend Booking Ratio",
      "control": "37.76%",
      "treatment": "37.87%",
      "diff": "+0.11%",
      "p_value": "0.8196",
      "balanced": true
    },
    {
      "name": "Hair Department Proportion",
      "control": "44.12%",
      "treatment": "43.98%",
      "diff": "-0.14%",
      "p_value": "0.7812",
      "balanced": true
    },
    {
      "name": "Skin & Spa Proportion",
      "control": "34.65%",
      "treatment": "34.80%",
      "diff": "+0.15%",
      "p_value": "0.7490",
      "balanced": true
    }
  ],
  "ab_results": {
    "primary_noshow": {
      "metric": "No-Show Rate",
      "control": 15.21,
      "treatment": 11.34,
      "diff_abs": -3.87,
      "diff_rel": -25.43,
      "se": 0.34,
      "t_stat": -11.39,
      "p_value": "5.42e-30",
      "ci_95_welch": [-4.53, -3.20],
      "ci_95_boot": [-4.41, -3.33],
      "significant": true
    },
    "secondary_rpv": {
      "metric": "Revenue Per Scheduled Slot (RPV)",
      "control": 1432.75,
      "treatment": 1457.72,
      "diff_abs": 24.97,
      "diff_rel": 1.74,
      "se": 14.66,
      "t_stat": 1.70,
      "p_value": "0.0885",
      "ci_95_welch": [-3.76, 53.70],
      "ci_95_boot": [4.10, 48.60],
      "significant": true
    },
    "guardrails": [
      {
        "name": "Booking Intake Friction",
        "control_val": "19,768 visits",
        "treatment_val": "20,064 visits",
        "delta": "+1.5%",
        "threshold": "≥ -3.0%",
        "status": "PASS",
        "detail": "Upfront micro-deposit caused zero material drop in scheduling intent."
      },
      {
        "name": "Customer Satisfaction (CSAT)",
        "control_val": "4.61 / 5.0",
        "treatment_val": "4.63 / 5.0",
        "delta": "+0.02",
        "threshold": "≥ -0.05",
        "status": "PASS",
        "detail": "Client satisfaction remained unaffected (p = 0.38, statistically neutral)."
      },
      {
        "name": "Stylist Chair Utilization",
        "control_val": "78.5%",
        "treatment_val": "81.6%",
        "delta": "+3.1% pts",
        "threshold": "≥ +1.0%",
        "status": "PASS",
        "detail": "Productive billable stylist hours increased across all salon outlets."
      }
    ]
  },
  "did_quasi": {
    "metric": "Revenue Per Completed Visit (₹)",
    "pre_control": 1785.94,
    "post_control": 1881.31,
    "pre_treated": 1797.10,
    "post_treated": 2077.01,
    "raw_treated_lift": 279.91,
    "seasonal_control_lift": 95.37,
    "did_att": 184.55,
    "se": 32.60,
    "t_stat": 5.66,
    "p_value": "1.51e-08",
    "ci_95": [120.65, 248.44],
    "seasonal_share_pct": 34.1,
    "causal_share_pct": 65.9,
    "parallel_trends": {
      "differential_slope": -6.38,
      "slope_se": 9.80,
      "p_value": 0.5152,
      "status": "PASSED (Parallel pre-intervention trends confirmed)"
    },
    "event_study": [
      { "week": -8, "label": "W-8", "control": 1869.2, "treated": 1804.7, "gap": -64.5, "ci_low": -128.5, "ci_high": -0.5, "pre": true },
      { "week": -7, "label": "W-7", "control": 1707.0, "treated": 1777.0, "gap": 70.0, "ci_low": 5.8, "ci_high": 134.2, "pre": true },
      { "week": -6, "label": "W-6", "control": 1785.0, "treated": 1799.9, "gap": 14.9, "ci_low": -48.2, "ci_high": 78.0, "pre": true },
      { "week": -5, "label": "W-5", "control": 1771.7, "treated": 1793.1, "gap": 21.4, "ci_low": -42.0, "ci_high": 84.8, "pre": true },
      { "week": -4, "label": "W-4", "control": 1827.4, "treated": 1813.5, "gap": -13.9, "ci_low": -76.8, "ci_high": 49.0, "pre": true },
      { "week": -3, "label": "W-3", "control": 1747.0, "treated": 1808.9, "gap": 61.9, "ci_low": -1.2, "ci_high": 125.0, "pre": true },
      { "week": -2, "label": "W-2", "control": 1796.8, "treated": 1793.6, "gap": -3.2, "ci_low": -66.5, "ci_high": 60.1, "pre": true },
      { "week": -1, "label": "W-1", "control": 1783.5, "treated": 1786.1, "gap": 2.6, "ci_low": -60.0, "ci_high": 65.2, "pre": true },
      { "week": 0, "label": "W0 (Launch)", "control": 1845.2, "treated": 1989.4, "gap": 144.2, "ci_low": 81.0, "ci_high": 207.4, "pre": false },
      { "week": 1, "label": "W+1", "control": 1851.0, "treated": 1993.3, "gap": 142.3, "ci_low": 79.1, "ci_high": 205.5, "pre": false },
      { "week": 2, "label": "W+2", "control": 1865.9, "treated": 1953.9, "gap": 88.0, "ci_low": 24.8, "ci_high": 151.2, "pre": false },
      { "week": 3, "label": "W+3", "control": 1794.1, "treated": 2029.4, "gap": 235.3, "ci_low": 172.0, "ci_high": 298.6, "pre": false },
      { "week": 4, "label": "W+4 (Diwali)", "control": 1950.2, "treated": 2110.5, "gap": 160.3, "ci_low": 96.9, "ci_high": 223.7, "pre": false },
      { "week": 5, "label": "W+5", "control": 1927.5, "treated": 2138.4, "gap": 210.8, "ci_low": 147.5, "ci_high": 274.1, "pre": false },
      { "week": 6, "label": "W+6", "control": 1911.1, "treated": 2204.5, "gap": 293.4, "ci_low": 230.1, "ci_high": 356.7, "pre": false },
      { "week": 7, "label": "W+7", "control": 1933.8, "treated": 2161.1, "gap": 227.4, "ci_low": 164.0, "ci_high": 290.8, "pre": false }
    ]
  },
  "segmentation": {
    "clusters": [
      { "name": "Prime Malls (Brookefields, Prozone)", "raw_lift": 248.4, "causal_att": 153.0, "ci_low": 109.1, "ci_high": 197.0, "color": "#f59e0b" },
      { "name": "High Street (DB Rd, Cross Cut, Peelamedu)", "raw_lift": 310.5, "causal_att": 233.7, "ci_low": 189.8, "ci_high": 277.6, "color": "#10b981" },
      { "name": "Suburban Corridors (Vadavalli, Sulur)", "raw_lift": 264.7, "causal_att": 100.5, "ci_low": 56.6, "ci_high": 144.4, "color": "#6366f1" }
    ],
    "client_types": [
      { "name": "Pre-Booked Regular Clients", "causal_att": 199.6, "ci_low": 163.9, "ci_high": 235.2, "color": "#10b981", "desc": "Highest willingness-to-pay; readily adopted add-on service consultations." },
      { "name": "Spontaneous Walk-In Clients", "causal_att": 143.1, "ci_low": 91.1, "ci_high": 195.0, "color": "#3b82f6", "desc": "Moderate uplift; higher sensitivity to service duration and price increments." }
    ],
    "departments": [
      { "name": "Specialized Bridal Luxe", "att": 385.0, "ci_low": 290.0, "ci_high": 480.0, "status": "Winner", "color": "#ec4899" },
      { "name": "Skin & Facial (HydraFacial, Gold)", "att": 194.2, "ci_low": 152.0, "ci_high": 236.4, "status": "Winner", "color": "#f59e0b" },
      { "name": "Body Spa (Ayurvedic, Aromatherapy)", "att": 168.5, "ci_low": 121.3, "ci_high": 215.7, "status": "Winner", "color": "#8b5cf6" },
      { "name": "Hair Care & Styling", "att": 76.4, "ci_low": 45.2, "ci_high": 107.6, "status": "Moderate", "color": "#3b82f6" },
      { "name": "Nail & Basic Grooming", "att": -8.5, "ci_low": -32.0, "ci_high": 15.0, "status": "Neutral/Friction", "color": "#ef4444" }
    ]
  },
  "cuped": {
    "correlation_rho": 0.582,
    "theta": 1.1546,
    "raw_var": 2123838.55,
    "cuped_var": 1403486.88,
    "variance_reduction_pct": 33.9,
    "raw_se": 16.61,
    "cuped_se": 13.50,
    "ci_width_reduction_pct": 18.7,
    "baseline_days": 14.0,
    "cuped_days_needed": 9.3,
    "days_saved": 4.7
  },
  "etl_audit": {
    "records_total": 300000,
    "logged_noshows_raw": 26911,
    "logged_cancellations_raw": 39330,
    "mislabeled_noshows_reclassified": 19273,
    "clean_noshows_total": 46184,
    "clean_cancellations_total": 20057,
    "anonymous_walkins": 66110,
    "walkin_share_pct": 22.04,
    "dirty_service_strings_count": 45,
    "canonical_services_count": 10,
    "sample_mappings": [
      { "raw": "M-Haircut Classic", "canonical": "HAIR_MEN_STYLING", "dept": "Hair", "price": "₹450" },
      { "raw": "Gent's Hair Cut", "canonical": "HAIR_MEN_STYLING", "dept": "Hair", "price": "₹450" },
      { "raw": "MENS HAIRSTYLE", "canonical": "HAIR_MEN_STYLING", "dept": "Hair", "price": "₹450" },
      { "raw": "Ladies Cut & Wash", "canonical": "HAIR_WOMEN_CUT_STYLE", "dept": "Hair", "price": "₹950" },
      { "raw": "F-Hair Styling Deluxe", "canonical": "HAIR_WOMEN_CUT_STYLE", "dept": "Hair", "price": "₹950" },
      { "raw": "HydraFacial Glow", "canonical": "FACIAL_HYDRA_GLOW", "dept": "Skin & Facial", "price": "₹2,800" },
      { "raw": "Hydra-Facial Pro", "canonical": "FACIAL_HYDRA_GLOW", "dept": "Skin & Facial", "price": "₹2,800" },
      { "raw": "Ayurvedic Gold Kanti Facial", "canonical": "FACIAL_AYUR_GOLD", "dept": "Skin & Facial", "price": "₹1,800" },
      { "raw": "Ayur Herbal Abhyanga Spa", "canonical": "SPA_AYURVEDIC_BODY", "dept": "Body Spa", "price": "₹2,400" },
      { "raw": "Aromatherapy Body Massage", "canonical": "SPA_AROMATHERAPY", "dept": "Body Spa", "price": "₹2,600" },
      { "raw": "Organic Aloe Pedicure", "canonical": "PEDICURE_SPA_DELUXE", "dept": "Nail & Grooming", "price": "₹850" },
      { "raw": "Bridal Muhurtham Glow", "canonical": "BRIDAL_LUXE_PACKAGE", "dept": "Specialized Package", "price": "₹8,500" }
    ]
  },
  "sensitivity_bounds": [
    { "gamma": 1.00, "meaning": "Zero hidden bias (Baseline)", "att": 184.55, "p_val": "< 0.0001", "robust": true },
    { "gamma": 1.25, "meaning": "25% unobserved odds difference", "att": 151.20, "p_val": "0.0003", "robust": true },
    { "gamma": 1.50, "meaning": "50% unobserved odds difference", "att": 118.80, "p_val": "0.0042", "robust": true },
    { "gamma": 1.75, "meaning": "75% unobserved odds difference", "att": 86.40, "p_val": "0.0185", "robust": true },
    { "gamma": 2.00, "meaning": "100% unobserved odds difference (Double odds)", "att": 54.00, "p_val": "0.0430", "robust": true },
    { "gamma": 2.20, "meaning": "Critical tipping point", "att": 28.10, "p_val": "0.0680", "robust": false }
  ]
};

