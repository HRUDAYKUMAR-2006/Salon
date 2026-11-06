# EXPERIMENT DESIGN DOCUMENT: SMART SLOT HOLD & DYNAMIC RECONFIRMATION PROTOCOL (SDRS)
**Organization:** BLXDES Salon & Spa Chain (22 Outlets, Coimbatore & Western Tamil Nadu)  
**Author:** Lead Causal Inference & Experimentation Data Scientist  
**Date:** November 2026  
**Document Version:** 1.0 (Production Master)  
**Status:** Executed & Concluded (Phase 1 Trial)

---

## 1. Executive Summary & Problem Context
BLXDES operates 22 salon and spa outlets across Coimbatore and neighboring Western Tamil Nadu districts, processing ~22,000 appointments monthly. In beauty and wellness service operations, **chair idle time** represents perishable inventory: when an appointment slot goes unfulfilled due to an unannounced **No-Show**, fixed stylist wages and real estate overhead cannot be recovered.

Historically, the chain suffered an unadjusted **18.5% no-show rate**, peaking at over 22% during high-demand weekend slots. Previous management interventions relied on manual phone calls from front-desk staff, which were inconsistent, unrecorded, and frequently resulted in misclassifying no-shows as cancellations.

To address this structural revenue leakage, the Product and Operations team designed the **Smart Dynamic Reconfirmation System (SDRS)**—an automated multi-touch WhatsApp interactive protocol combined with a micro-deposit requirement (₹100) for peak weekend slots, backed by a 1-click seamless reschedule feature.

---

## 2. Hypothesis Formulation

### 2.1 Primary Hypothesis
* **Null Hypothesis ($H_0$):** The introduction of the Smart Dynamic Reconfirmation System (SDRS) produces no difference in the client no-show rate compared to standard SMS reminders:
  $$\mu_{\text{no-show, SDRS}} = \mu_{\text{no-show, Control}}$$
* **Alternative Hypothesis ($H_1$):** The SDRS protocol reduces the client no-show rate by at least 3.0 percentage points (a relative drop $\ge 16.2\%$):
  $$\mu_{\text{no-show, SDRS}} < \mu_{\text{no-show, Control}} - 0.030$$

### 2.2 Secondary Revenue Hypothesis
* **Null Hypothesis ($H_{0,\text{rev}}$):** Reclaiming unfilled slots does not materially impact net Revenue Per Scheduled Appointment (RPV).
* **Alternative Hypothesis ($H_{1,\text{rev}}$):** Net RPV will increase by $\ge ₹50$ due to higher chair completion and backfilling of cancelled slots.

---

## 3. Metric Taxonomy & Guardrail Framework

| Metric Tier | Metric Name | Definition & Formula | Target / MDE | Directional Goal |
| :--- | :--- | :--- | :--- | :--- |
| **Primary (OEC)** | **No-Show Rate (%)** | $\frac{\text{Appointments with No-Show Status}}{\text{Total Scheduled Appointments}}$ | $-3.0\%$ abs ($-16.2\%$ rel) | Decrease (Down is Good) |
| **Secondary** | **Revenue Per Visit (₹ RPV)** | $\frac{\sum \text{Total Revenue (Service + Product)}}{\text{Total Scheduled Appointments}}$ | $+₹50.00$ ($+3.5\%$) | Increase |
| **Secondary** | **Stylist Chair Utilization (%)** | $\frac{\sum \text{Completed Service Duration (Hours)}}{\sum \text{Scheduled Stylist Shift Hours}}$ | $+4.0\%$ abs | Increase |
| **Guardrail 1** | **Booking Funnel Volume** | Total unique appointments initiated per week | $\le -3.0\%$ max friction | Neutral / No Material Drop |
| **Guardrail 2** | **Client Satisfaction (CSAT)** | Post-visit 5-star rating (1.0 to 5.0) | $\Delta \text{CSAT} \ge -0.05$ | Maintain ($\ge 4.60$) |
| **Guardrail 3** | **Advance Cancellation Velocity** | $\%$ cancellations notified $\ge 4$ hours prior | $+15.0\%$ abs | Increase (Enables Backfill) |

---

## 4. Power Analysis & Sample Size Sizing

### 4.1 Statistical Parameters
* **Significance Level ($\alpha$):** $0.05$ (two-tailed, Type I error rate)
* **Statistical Power ($1 - \beta$):** $0.80$ (Type II error rate $\beta = 0.20$)
* **Baseline No-Show Proportion ($p_1$):** $0.185$ (18.5%)
* **Minimum Detectable Effect (MDE, $p_1 - p_2$):** $0.030$ (3.0% abs reduction $\rightarrow p_2 = 0.155$)

### 4.2 Sample Size Formula (Two-Proportion Z-Test)
$$n = \frac{\left( Z_{1-\alpha/2}\sqrt{2\bar{p}(1-\bar{p})} + Z_{1-\beta}\sqrt{p_1(1-p_1) + p_2(1-p_2)} \right)^2}{(p_1 - p_2)^2}$$
Where:
* $Z_{1-\alpha/2} = 1.95996$
* $Z_{1-\beta} = 0.84162$
* $\bar{p} = \frac{0.185 + 0.155}{2} = 0.170$

### 4.3 Sizing Results
* **Required Sample per Variant ($n$):** **2,465 appointments**
* **Total Sample Required ($2n$):** **4,930 appointments**
* **Eligible Appointment Traffic:** ~1,400 appointments/day across participating salons
* **Statistical Horizon:** ~3.5 days of traffic
* **Recommended Run Duration:** **14 full days (2 complete weekly cycles)** to account for day-of-week seasonality (Friday-Sunday traffic vs Tuesday lull) and stylist shift rotations.

### 4.4 Cluster Randomization & Design Effect (ICC) Consideration
If randomizing at the **outlet level** rather than the client booking level:
$$\text{Design Effect } (DE) = 1 + (m - 1)\rho$$
With average cluster size $m \approx 65$ appointments/day/outlet and intra-cluster correlation coefficient (ICC) $\rho \approx 0.035$:
$$DE = 1 + (64 \times 0.035) = 3.24$$
*Cluster randomization would require inflating the sample size by $3.24\times$ (approx 15,970 appointments or 6 weeks of testing).*  
**Architectural Decision:** Implement **user/booking-level hash randomization** stratified by salon outlet and day-of-week to maintain unit independence and eliminate cluster inflation.

---

## 5. Randomization Strategy & SUTVA Integrity

### 5.1 Assignment Engine
* **Randomization Unit:** Unique Client Booking Token (hash salt: `md5(client_id + appointment_date + "SDRS_V1") % 100`).
* **Ratio:** 50% Control : 50% Treatment.
* **Stratification:** Stratified by Outlet Tier (Prime Mall, High Street, Suburban) and Day-of-Week (Weekday vs Weekend).

### 5.2 SUTVA (Stable Unit Treatment Value Assumption) Mitigation
* **Spillover / Contamination Risk:** Stylists operating across both treatment and control clients could alter behavior (e.g., calling control clients manually).  
  *Mitigation:* Stylists were blinded to the assignment mechanism. The automated WhatsApp engine handled reconfirmations server-side without manual stylist intervention.
* **Slot Displacement Risk:** When a treatment client cancels 4 hours early via the 1-click link, that slot is released into the general pool, potentially benefiting both groups.  
  *Mitigation:* Slot backfill tracking measured whether reclaimed slots were filled by walk-ins or waitlist clients.

---

## 6. Real-World Dirty Data Protocols

1. **Reclassifying Misclassified Cancellations:**
   Receptionists frequently press "Cancel" instead of "No-Show" when clients fail to show up. Any appointment marked "Cancelled" within 30 minutes of scheduled start or post-start without advance notice is programmatic reconciliated into "No-Show".
2. **Service Catalog Standardization:**
   All 48 outlet-specific dirty strings are fuzzy-mapped into 10 canonical service codes across 4 primary departments (Hair, Skin/Facial, Spa, Nail/Grooming).
3. **Walk-in Handling:**
   Spontaneous walk-ins lacking client IDs are assigned deterministic proxy IDs (`PRX_WALKIN_{OUTLET}_{HASH}`) and tagged with `is_walkin = 1`.

---

## 7. Variance Reduction Plan: CUPED Implementation
To accelerate future test iterations and reduce the required sample size, pre-experiment historical 90-day spend ($X$) is leveraged as a baseline covariate for post-experiment appointment revenue ($Y$):
$$\tilde{Y}_{\text{CUPED}} = Y - \theta (X - \mathbb{E}[X]), \quad \text{where } \theta = \frac{\text{Cov}(Y, X)}{\text{Var}(X)}$$
* Target correlation: $\rho(X, Y) \ge 0.55$.
* Target variance reduction: $1 - \rho^2 \approx 30\% - 40\%$.
* Target test duration reduction: Shortens required testing window from 14 days down to 9 days.

---

## 8. Decision Thresholds & Recommendation Rubric

| Scenario | Primary Metric (No-Show Rate) | Guardrail 1 (Bookings) | Guardrail 2 (CSAT) | Final Business Action |
| :--- | :--- | :--- | :--- | :--- |
| **Green Light (Go)** | Statistically significant drop $\ge -3.0\%$ ($p < 0.05$) | Drop $\le -3.0\%$ | $\Delta \text{CSAT} \ge -0.05$ | **GO:** Full chain rollout across all 22 outlets. |
| **Amber Light (Extend)** | Drop between $-1.5\%$ and $-3.0\%$ ($p < 0.10$) | Neutral | Neutral | **EXTEND:** Run for an additional 7 days with CUPED adjustment. |
| **Red Light (No-Go)** | Statistically indistinguishable ($p \ge 0.10$) | Severe friction ($> -5.0\%$) | Statistically significant drop | **NO-GO:** Kill initiative; revert to standard SMS reminders. |

