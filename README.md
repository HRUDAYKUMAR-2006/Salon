# BLXDES SALON & SPA: CAUSAL INFERENCE & EXPERIMENTATION PLATFORM
### *De-Confounding Festive Seasonality, Designing Robust A/B Tests, and Estimating True Business Value*

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Causal Inference](https://img.shields.io/badge/Econometrics-DiD%20%7C%20CUPED-emerald.svg)]()
[![Sample Size](https://img.shields.io/badge/Records-300%2C000%20Transactions-gold.svg)]()
[![Decision](https://img.shields.io/badge/Decision%20Verdict-GO%20(Full%20Rollout)-green.svg)]()

---

## 1. Executive Summary & Problem Formulation
A premier salon & spa chain with **22 outlets across Coimbatore and Western Tamil Nadu** launched an operational and menu package revamp in Q4. Leadership observed a **+15.6% raw revenue increase (+₹279.91 per visit)** and claimed significant success. 

However, Q4 in Tamil Nadu coincides with **Navaratri, Diwali, Karthigai Deepam, and auspicious Muhurtham wedding dates**. Management failed to verify whether the improvement was genuine causal lift or merely passive festive seasonality.

Furthermore, perishable chair capacity suffered from an unadjusted **18.5% no-show rate**, with operational front-desk logs corrupted by **no-shows marked as cancellations**, **48 fragmented service names**, and **anonymous walk-ins**.

### Core Deliverables Achieved:
1. **Quasi-Experiment (Difference-in-Differences):** Evaluated last quarter's change against 4 matched Western TN control outlets (Tiruppur & Erode). Proved that **34.1% of the raw gain (+₹95.37) was purely seasonal**, while the **true causal ATT was +₹184.55** ($p < 0.001$), with robust parallel pre-trends ($p = 0.5152$).
2. **Data Cleaning & ETL Engine:** Audited 300,000 transactions, reconciliated **19,273 false cancellations** into true no-shows, harmonized 45 dirty service strings into 10 canonical offerings, and resolved 66,110 anonymous walk-ins.
3. **Prospective A/B Experiment Design:** Formulated hypotheses, conducted power analysis ($\alpha = 0.05, 1-\beta = 0.80$, MDE $-3.0\%$ abs), checked Sample Ratio Mismatch ($\chi^2 = 2.20, p = 0.138$), verified covariate balance, and estimated a **$-3.87\%$ absolute drop in no-shows ($-25.4\%$ relative, $p < 10^{-29}$)** with 95% bootstrap intervals.
4. **Variance Reduction (CUPED):** Leveraged pre-experiment 90-day spend ($\rho = 0.582$) to achieve **33.9% variance reduction**, shrinking standard error by 18.7% and reducing test duration from **14 days to 9.3 days (saving 4.7 days)**.
5. **Interactive Full-Stack Web Application:** Interactive dashboard with decision memos, DiD event-study charts, CUPED simulators, live SRM testing, and dynamic power sizing tools.

---

## 2. Key Statistical Results & Confidence Intervals

| Analysis Stream | Metric Evaluated | Control / Baseline | Treatment / Post | Estimated Delta / ATT | 95% Confidence Interval | p-value | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Quasi-Experiment (DiD)** | Revenue Per Completed Visit (₹) | ₹1,785.94 $\rightarrow$ ₹1,881.31 | ₹1,797.10 $\rightarrow$ ₹2,077.01 | **+₹184.55 (True ATT)** | **[+₹120.65, +₹248.44]** | $p = 1.51 \times 10^{-8}$ | Statistically Significant |
| *Festive Seasonality* | Control Region Pure Lift | ₹1,785.94 | ₹1,881.31 | **+₹95.37 (Seasonal)** | [+₹54.20, +₹136.50] | $p < 0.001$ | Explains 34.1% of Lift |
| *Parallel Trends Test* | Pre-Trend Differential Slope | N/A | N/A | **-₹6.38 / week** | [-₹25.80, +₹13.04] | $p = 0.5152$ | **PASSED (Trends Parallel)** |
| **Prospective A/B Test** | **No-Show Rate (%)** | **15.21%** | **11.34%** | **-3.87% pts (-25.4%)** | **[-4.41%, -3.33%]** | $p = 5.42 \times 10^{-30}$ | **PASSED (OEC Primary)** |
| *Live SRM Test* | Assignment Traffic Split | 19,768 (49.63%) | 20,064 (50.37%) | Expected: 50:50 | $\chi^2 = 2.1996$ | $p = 0.1380$ | **PASSED (No SRM)** |
| *Secondary Metric* | Revenue Per Scheduled Slot | ₹1,432.75 | ₹1,457.72 | **+₹24.97 (+1.7%)** | [-₹3.76, +₹53.70] | $p = 0.0885$ | Reclaimed Capacity Lift |
| **Variance Reduction** | CUPED Standard Error (₹) | ±₹16.61 (Raw OLS) | ±₹13.50 (CUPED) | **-18.7% CI Width** | Test cut 14d $\rightarrow$ 9.3d | $\rho = 0.582$ | **33.9% Var Reduction** |

---

## 3. Directory Structure
```
c:\hrudaykumar\Salon\
├── data/
│   ├── raw/
│   │   ├── appointments_raw.csv           # 300,000 raw appointment transactions
│   │   ├── outlets_metadata.csv           # 22 outlets (18 Coimbatore + 4 Control)
│   │   └── stylists.csv                   # Stylist directory and seniority
│   └── processed/
│       ├── clean_master_appointments.csv  # Cleaned, reconciled master table
│       ├── ab_experiment_clean.csv        # Prospective A/B trial dataset
│       ├── did_quasi_experiment.csv       # 8-wk pre/post DiD event window
│       └── metrics_summary.json           # Exported statistical metrics & CIs
├── pipeline/
│   ├── 01_generate_salon_dataset.py       # Simulates realistic messy operations
│   ├── 02_data_cleaning_etl.py            # Reclassification, fuzzy harmonization
│   ├── 03_causal_inference_engine.py      # DiD, A/B, bootstrap, CUPED, SRM
│   └── 04_create_notebook.py              # Compiles Jupyter notebook
├── notebooks/
│   └── salon_causal_analysis.ipynb        # Complete reproducible Jupyter analysis
├── docs/
│   ├── EXPERIMENT_DESIGN_DOC.md           # Formal experiment design & power sizing
│   ├── ONE_PAGE_DECISION_MEMO.md          # Executive 1-page decision memo
│   └── CAUSAL_THREATS_AND_VALIDITY.md     # Threats to validity & failure modes
├── web/
│   ├── index.html                         # Interactive Web Application
│   ├── css/style.css                      # Luxury dark salon aesthetic stylesheet
│   └── js/
│       ├── data.js                        # Embedded statistical outputs
│       ├── charts.js                      # Chart.js visualizations
│       └── app.js                         # Dynamic calculators, sliders, handlers
├── server.py                              # Local HTTP server launcher
└── README.md                              # Consolidated master documentation
```

---

## 4. How to Run the Platform

### Step 1: Run Full Analytical Pipelines
```powershell
# 1. Generate the raw 300,000-record dataset
python pipeline/01_generate_salon_dataset.py

# 2. Run ETL cleaning & dirty-data reconciliation
python pipeline/02_data_cleaning_etl.py

# 3. Execute econometrics & causal inference engine
python pipeline/03_causal_inference_engine.py

# 4. Generate the Jupyter Notebook
python pipeline/04_create_notebook.py
```

### Step 2: Launch the Interactive Web Platform
```powershell
python server.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your web browser.

---

## 5. Summary of Decision & Strategic Recommendation
* **Verdict:** **GO (Full Chain-Wide Rollout)**
* **Annualized Net Contribution:** **+₹1.59 Crore ($192,000 USD, 2,948% ROI)**
* **Phased Rollout:**
  - *Phase 1 (Days 1–10):* 4 Tier A Prime Mall Salons (Brookefields, Prozone, Race Course, RS Puram North).
  - *Phase 2 (Days 11–20):* 8 High-Street Salons (Gandhipuram, DB Road, Saibaba Colony, Peelamedu).
  - *Phase 3 (Days 21–30):* 6 Suburban Salons with dynamic deposit waivers for off-peak walk-ins.

