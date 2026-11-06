# EXECUTIVE DECISION MEMO: CAUSAL IMPACT & EXPERIMENTATION VERDICT
**To:** Board of Directors & Chief Operating Officer, BLXDES Salon & Spa Chain  
**From:** Lead Causal Inference & Analytics Lead  
**Date:** November 2026  
**Subject:** Causal Audit of Q4 Business Change & Prospective A/B Test Verdict for SDRS Rollout  

---

### 1. EXECUTIVE ACTION RECOMMENDATION: **FULL GO (CHAIN-WIDE ROLLOUT)**
We recommend an immediate, phased chain-wide rollout of the **Smart Dynamic Reconfirmation System (SDRS)** across all 22 outlets, supported by an annualized net profit uplift of **₹1.59 Crore ($192,000 USD, ROI: 2,948%)**. Furthermore, our causal audit reveals that management's previously claimed Q4 uplift was **over-estimated by 34.1%** due to unadjusted festive seasonality.

---

### 2. CORE EMPIRICAL FINDINGS & CONFIDENCE INTERVALS

| Analysis Stream | Metric Evaluated | Naive / Claimed Value | True Causal Estimate | 95% Confidence Interval | Statistical Significance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Q4 Retrospective Change** | Revenue Per Visit (RPV) | $+₹279.91$ ($+15.6\%$) | **$+₹184.55$ ($+10.3\%$)** | **[+₹120.70, +₹248.40]** | $p < 0.001$ (DiD TWFE) |
| *Festive Seasonality Share* | Control Outlet Natural Lift | *Ignored by leadership* | **$+₹95.37$ ($+5.3\%$)** | [+₹54.20, +₹136.50] | $p < 0.001$ |
| **Prospective A/B Test** | **No-Show Rate (%)** | N/A (Live Trial) | **$-3.87\%$ abs ($-25.4\%$ rel)** | **[-4.41%, -3.33%]** | $p = 5.42 \times 10^{-30}$ |
| **Prospective A/B Test** | Revenue Per Scheduled Slot | N/A (Live Trial) | **$+₹72.40$ ($+4.7\%$)** | **[+₹48.10, +₹96.70]** | $p < 0.001$ |
| **Variance Reduction (CUPED)**| Standard Error Compression | N/A | **$-18.7\%$ narrower CI** | Test cut from 14d $\rightarrow$ 9.3d | $33.9\%$ Var Reduction |

---

### 3. METHODOLOGICAL RIGOR & ASSUMPTION CHECKS
1. **Parallel Trends Validated ($p = 0.5152$):** In the 8 weeks preceding Q4 rollout, revenue trends between Coimbatore outlets and Western TN control outlets (Tiruppur/Erode) moved synchronously (differential slope: $-₹6.38$/week, $t = -0.65$, not significant). The divergence occurred strictly upon intervention.
2. **Sample Ratio Mismatch (SRM) Passed ($p = 0.1380$):** The prospective A/B test assigned 19,768 Control vs 20,064 Treatment units. Chi-square test ($\chi^2 = 2.20$) confirmed zero traffic diversion or assignment bias.
3. **Guardrail Metrics Intact:** Total booking friction was $-0.8\%$ (well within the $-3.0\%$ guardrail threshold), while Client CSAT was unaffected (4.61 Control vs 4.63 Treatment, $p = 0.38$). Stylist chair utilization improved by $+3.8$ percentage points.

---

### 4. WINNING VS VULNERABLE SEGMENTS (HETEROGENEOUS EFFECTS)
* **High-Margin Winners:** Prime Mall outlets (Brookefields, Prozone: **$+₹214.20$ ATT**) and Skin/Facial & Spa services (HydraFacial, Ayurvedic Spa: **$+₹194.20$ ATT**) captured the greatest willingness-to-pay.
* **Vulnerable / Friction Cohort:** Walk-ins in Suburban outlets (Sulur, Kuniyamuthur) exhibited sensitivity to upfront micro-deposits (ATT: $+₹32.10$, close to neutral).  
  *Operational Mitigation:* Enable dynamic deposit waiver for walk-in arrivals during off-peak weekday hours.

---

### 5. FINANCIAL MODEL & 12-MONTH P&L IMPACT

| Line Item | Unit Value | Monthly Chain Total (22 Outlets) | Annualized Run-Rate |
| :--- | :--- | :--- | :--- |
| Reclaimed No-Show Appointments | +43 appointments / store | **946 slots recovered** | **11,352 slots / year** |
| Average Reclaimed Ticket Value | ₹1,450 / appointment | +₹13,71,700 gross | **₹1,64,60,400 gross** |
| WhatsApp API & Software Infrastructure | ₹2,045 / store | -₹45,000 SaaS fees | -₹5,40,000 operating cost |
| **Net Incremental Profit Contribution** | **EBITDA Accretive** | **+₹13,26,700 / month** | **+₹1,59,20,400 Net / Year** |

---

### 6. PHASED ROLLOUT SCHEDULE
* **Phase 1 (Days 1–10):** Deploy to 4 Tier A Prime Mall Outlets (Brookefields, Prozone, Race Course, RS Puram North).
* **Phase 2 (Days 11–20):** Deploy to 8 High-Street Commercial Outlets (Gandhipuram, DB Road, Saibaba Colony, Peelamedu).
* **Phase 3 (Days 21–30):** Deploy to remaining Suburban outlets with auto-adaptive deposit rules for walk-in clients.

