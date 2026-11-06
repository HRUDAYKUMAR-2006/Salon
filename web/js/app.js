// Kongu Luxe Causal Analytics - Interactive Application Logic

document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  populateScorecards();
  setupPowerCalculator();
  setupSrmCalculator();
  setupCupedSimulator();
  setupSensitivitySlider();
  setupDirtyDataSearch();
  setupDocTabs();
  
  // Initialize charts after DOM layout settles
  setTimeout(() => {
    if (typeof initializeAllCharts === 'function') {
      initializeAllCharts();
    }
  }, 100);
});

// 1. Navigation & Tab Switching
function setupNavigation() {
  const navButtons = document.querySelectorAll('.nav-btn');
  const sections = document.querySelectorAll('.dashboard-section');

  navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.dataset.target;
      navButtons.forEach(b => b.classList.remove('active'));
      sections.forEach(s => s.classList.remove('active'));

      btn.classList.add('active');
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.classList.add('active');
        // Refresh charts inside that section
        setTimeout(() => {
          if (targetId === 'sec-did') {
            renderWaterfallChart();
            renderEventStudyChart();
          } else if (targetId === 'sec-ab') {
            renderBootstrapChart();
          } else if (targetId === 'sec-segments') {
            renderForestPlot();
          } else if (targetId === 'sec-cuped') {
            renderCupedChart();
          } else if (targetId === 'sec-power') {
            renderPowerCurveChart();
          }
        }, 80);
      }
    });
  });
}

// 2. Populate Static KPI Cards & Tables
function populateScorecards() {
  const d = SALON_DATA;

  // Header badges
  const headerTotalRecords = document.getElementById('hdrTotalRecords');
  if (headerTotalRecords) headerTotalRecords.innerText = d.summary.raw_records_analyzed.toLocaleString();

  // Populate Balance Table
  const balanceBody = document.getElementById('balanceTableBody');
  if (balanceBody) {
    balanceBody.innerHTML = d.covariate_balance.map(row => `
      <tr>
        <td class="font-medium">${row.name}</td>
        <td>${row.control}</td>
        <td>${row.treatment}</td>
        <td class="font-bold text-accent">${row.diff}</td>
        <td>${row.p_value}</td>
        <td><span class="badge badge-success"><i class="fa fa-check"></i> Balanced</span></td>
      </tr>
    `).join('');
  }

  // Populate Guardrails
  const guardrailContainer = document.getElementById('guardrailsList');
  if (guardrailContainer) {
    guardrailContainer.innerHTML = d.ab_results.guardrails.map(g => `
      <div class="guardrail-card">
        <div class="guardrail-head">
          <span class="guardrail-title">${g.name}</span>
          <span class="badge badge-success">${g.status}</span>
        </div>
        <div class="guardrail-metrics">
          <div><small>Control:</small> <strong>${g.control_val}</strong></div>
          <div><small>Treatment:</small> <strong>${g.treatment_val}</strong></div>
          <div><small>Delta:</small> <strong class="text-emerald">${g.delta}</strong></div>
        </div>
        <p class="guardrail-detail">${g.detail} (Threshold: ${g.threshold})</p>
      </div>
    `).join('');
  }

  // Populate ETL sample mappings
  const etlTable = document.getElementById('etlMappingTable');
  if (etlTable) {
    etlTable.innerHTML = d.etl_audit.sample_mappings.map(m => `
      <tr>
        <td><code>${m.raw}</code></td>
        <td><span class="badge badge-indigo">${m.canonical}</span></td>
        <td>${m.dept}</td>
        <td><strong>${m.price}</strong></td>
      </tr>
    `).join('');
  }
}

// 3. Interactive Power & Sample Size Calculator
function setupPowerCalculator() {
  const baselineInput = document.getElementById('calcBaseline');
  const mdeInput = document.getElementById('calcMde');
  const powerInput = document.getElementById('calcPower');
  const trafficInput = document.getElementById('calcTraffic');
  const iccToggle = document.getElementById('calcClusterIcc');

  const outSampleVariant = document.getElementById('calcResVariant');
  const outSampleTotal = document.getElementById('calcResTotal');
  const outDays = document.getElementById('calcResDays');
  const outStatus = document.getElementById('calcResStatus');

  function recalculate() {
    const p1 = parseFloat(baselineInput.value) / 100;
    const mdeAbs = parseFloat(mdeInput.value) / 100;
    const targetP = p1 - mdeAbs;
    const power = parseFloat(powerInput.value) / 100;
    const dailyTraffic = parseInt(trafficInput.value) || 1400;
    const useCluster = iccToggle ? iccToggle.checked : false;

    // Display labels
    document.getElementById('lblBaseline').innerText = (p1 * 100).toFixed(1) + '%';
    document.getElementById('lblMde').innerText = '-' + (mdeAbs * 100).toFixed(1) + '%';
    document.getElementById('lblPower').innerText = (power * 100).toFixed(0) + '%';
    document.getElementById('lblTraffic').innerText = dailyTraffic.toLocaleString() + ' / day';

    const z_alpha = 1.95996; // alpha = 0.05
    // Z_beta calculation
    let z_beta = 0.8416; // default 80%
    if (power >= 0.90) z_beta = 1.2816;
    if (power >= 0.95) z_beta = 1.6449;

    const p_pool = (p1 + targetP) / 2;
    const num = Math.pow(z_alpha * Math.sqrt(2 * p_pool * (1 - p_pool)) + z_beta * Math.sqrt(p1 * (1 - p1) + targetP * (1 - targetP)), 2);
    const den = Math.pow(p1 - targetP, 2);
    let n_variant = Math.ceil(num / den);

    let designEffect = 1.0;
    if (useCluster) {
      const avgStoreSize = 65;
      const icc = 0.035;
      designEffect = 1 + (avgStoreSize - 1) * icc;
      n_variant = Math.ceil(n_variant * designEffect);
    }

    const n_total = n_variant * 2;
    const days = Math.max(14, Math.ceil(n_total / dailyTraffic));

    outSampleVariant.innerText = n_variant.toLocaleString();
    outSampleTotal.innerText = n_total.toLocaleString();
    outDays.innerText = days + ' Days';

    if (useCluster) {
      outStatus.innerHTML = `<span class="text-amber">⚠️ Cluster-Randomized (Design Effect = ${designEffect.toFixed(2)}x): Sample inflated to prevent false positives from store-level correlation.</span>`;
    } else {
      outStatus.innerHTML = `<span class="text-emerald">✓ User-Level Hash Randomization: High statistical efficiency; 14-day minimum handles 2 full weekly cycles.</span>`;
    }

    renderPowerCurveChart(p1, 0.05);
  }

  [baselineInput, mdeInput, powerInput, trafficInput].forEach(inp => {
    if (inp) inp.addEventListener('input', recalculate);
  });
  if (iccToggle) iccToggle.addEventListener('change', recalculate);

  recalculate();
}

// 4. Sample Ratio Mismatch (SRM) Live Checker
function setupSrmCalculator() {
  const ctrlInput = document.getElementById('srmCtrlInput');
  const treatInput = document.getElementById('srmTreatInput');
  const runBtn = document.getElementById('srmRunBtn');
  const resultDiv = document.getElementById('srmResultDiv');

  if (!runBtn) return;

  runBtn.addEventListener('click', () => {
    const oC = parseInt(ctrlInput.value);
    const oT = parseInt(treatInput.value);
    const total = oC + oT;
    const eC = total / 2;
    const eT = total / 2;

    const chi2 = (Math.pow(oC - eC, 2) / eC) + (Math.pow(oT - eT, 2) / eT);
    // Approximation for 1 df chi-square p-value:
    // P(X >= chi2) = 2 * (1 - Phi(sqrt(chi2)))
    const z = Math.sqrt(chi2);
    const t = 1.0 / (1.0 + 0.2316419 * z);
    const d = 0.3989423 * Math.exp(-z * z / 2.0);
    const prob = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
    const p_value = 2.0 * prob;

    const isMismatch = p_value < 0.01;

    resultDiv.innerHTML = `
      <div class="result-banner ${isMismatch ? 'banner-alert' : 'banner-success'}">
        <div class="banner-icon">${isMismatch ? '🚨' : '✅'}</div>
        <div class="banner-body">
          <h4>${isMismatch ? 'CRITICAL ALERT: Sample Ratio Mismatch (SRM) Detected!' : 'SRM PASSED: No Traffic Distortion'}</h4>
          <p>
            Observed Counts: Control = <strong>${oC.toLocaleString()}</strong> (${((oC/total)*100).toFixed(2)}%), 
            Treatment = <strong>${oT.toLocaleString()}</strong> (${((oT/total)*100).toFixed(2)}%)<br>
            Pearson Chi-Square Statistic ($\chi^2$): <strong>${chi2.toFixed(4)}</strong> | p-value: <strong>${p_value.toFixed(5)}</strong>
          </p>
          <p class="banner-subtext">
            ${isMismatch 
              ? 'Recommendation: DO NOT TRUST METRIC LIFTS. Investigate tracking drop-off, server timeouts, or routing filter bugs before analyzing.' 
              : 'Traffic split is mathematically consistent with true 50:50 allocation (p ≥ 0.01). Proceed with treatment effect estimation.'}
          </p>
        </div>
      </div>
    `;
  });
}

// 5. CUPED Interactive Simulator
function setupCupedSimulator() {
  const slider = document.getElementById('cupedRhoSlider');
  const rhoVal = document.getElementById('cupedRhoVal');
  const varRedPct = document.getElementById('cupedVarRedPct');
  const daysNeeded = document.getElementById('cupedDaysNeeded');
  const daysSaved = document.getElementById('cupedDaysSaved');

  if (!slider) return;

  slider.addEventListener('input', () => {
    const rho = parseFloat(slider.value);
    rhoVal.innerText = rho.toFixed(2);

    const varReduction = Math.pow(rho, 2) * 100;
    const baseDays = 14.0;
    const needed = baseDays * (1 - (varReduction / 100));
    const saved = baseDays - needed;

    varRedPct.innerText = varReduction.toFixed(1) + '%';
    daysNeeded.innerText = needed.toFixed(1) + ' Days';
    daysSaved.innerText = saved.toFixed(1) + ' Days';
  });
}

// 6. Rosenbaum Bounds Sensitivity Slider
function setupSensitivitySlider() {
  const slider = document.getElementById('gammaSlider');
  const gammaVal = document.getElementById('gammaVal');
  const robustVerdict = document.getElementById('gammaVerdict');
  const bounds = SALON_DATA.sensitivity_bounds;

  if (!slider) return;

  slider.addEventListener('input', () => {
    const g = parseFloat(slider.value);
    gammaVal.innerText = 'Γ = ' + g.toFixed(2);

    // Find nearest bound
    let match = bounds[0];
    for (let b of bounds) {
      if (Math.abs(b.gamma - g) < Math.abs(match.gamma - g)) {
        match = b;
      }
    }

    if (match.robust) {
      robustVerdict.innerHTML = `
        <span class="text-emerald font-bold">ROBUST (p = ${match.p_val})</span>: 
        Even if an unobserved factor increases treatment odds by ${Math.round((g - 1) * 100)}%, the causal lift remains positive and statistically significant (+₹${match.att.toFixed(1)} ATT).
      `;
    } else {
      robustVerdict.innerHTML = `
        <span class="text-rose font-bold">TIPPING POINT REACHED (p = ${match.p_val})</span>: 
        An unobserved confounder with odds ratio Γ ≥ ${g.toFixed(2)} could explain away the observed effect.
      `;
    }
  });
}

// 7. Dirty Data Search in ETL Studio
function setupDirtyDataSearch() {
  const searchInput = document.getElementById('dirtySearchInput');
  const table = document.getElementById('etlMappingTable');
  if (!searchInput || !table) return;

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    const rows = table.getElementsByTagName('tr');

    for (let row of rows) {
      const text = row.innerText.toLowerCase();
      row.style.display = text.includes(query) ? '' : 'none';
    }
  });
}

// 8. Documentation Viewer Tabs
function setupDocTabs() {
  const docBtns = document.querySelectorAll('.doc-tab-btn');
  const docPanes = document.querySelectorAll('.doc-pane');

  docBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.doc;
      docBtns.forEach(b => b.classList.remove('active'));
      docPanes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const pane = document.getElementById(target);
      if (pane) pane.classList.add('active');
    });
  });
}

