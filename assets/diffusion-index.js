(function () {
  "use strict";

  const COMPUTED_URL = "index/computed.v1.0.json";
  const SERIES_URL = "index/series.csv";

  const PILLAR_LABELS = {
    deployment: "Company adoption",
    cost_to_serve: "Reliable task completion",
    capital_intensity: "Capital commitments",
    labour_reorganisation: "Labour reorganisation",
    governance_burden: "Governance burden",
    human_capital: "Human capital",
    ecological_balance: "Ecological balance",
    energy_capacity: "Energy and grid capacity",
    ownership_distribution: "Ownership distribution",
    market_openness: "Market openness",
  };
  const PILLAR_ORDER = Object.keys(PILLAR_LABELS);
  const BLOCKS = {
    A: ["deployment", "cost_to_serve", "capital_intensity"],
    B: ["energy_capacity", "governance_burden", "human_capital", "market_openness"],
    C: ["labour_reorganisation", "ownership_distribution", "ecological_balance"],
  };
  const SECTOR_LABELS = {
    professional_services: "Professional and scientific services",
    software: "Information and software",
    manufacturing: "Manufacturing",
    agriculture: "Agriculture and forestry",
    healthcare: "Healthcare and social work",
    education: "Education and research",
    public_administration: "Public administration",
    finance_insurance: "Finance and insurance",
    retail_logistics: "Retail and transport",
    energy_utilities: "Energy and utilities",
  };
  const SECTOR_ORDER = Object.keys(SECTOR_LABELS);
  const POP_LABELS = { EU27: "EU27", FI: "Finland" };

  let DATA = null;
  let SERIES = [];
  let currentPop = "EU27";

  function roundHalfUp(value, places) {
    if (value === null || value === undefined || value === "") return null;
    const n = Number(value);
    if (!Number.isFinite(n)) return null;
    const dec = Number.parseInt(String(places), 10);
    const factor = 10 ** dec;
    const signed = n < 0 ? -1 : 1;
    return (signed * Math.floor(Math.abs(n) * factor + 0.5)) / factor;
  }

function formatNumber(value, places) {
    const n = roundHalfUp(value, places);
    if (n === null) return "—";
    return Number(n).toFixed(places);
  }

  function getPath(obj, path) {
    if (!obj || !path) return undefined;
    const parts = path.split(".");
    let cur = obj;
    for (let i = 0; i < parts.length; i += 1) {
      if (cur === null || cur === undefined) return undefined;
      const key = parts[i];
      if (key === "pillars" && Array.isArray(cur.pillars) && parts[i + 1] && !/^\d+$/.test(parts[i + 1])) {
        const id = parts[i + 1];
        cur = cur.pillars.find((p) => p.id === id);
        i += 1;
        continue;
      }
      cur = cur[key];
    }
    return cur;
  }

  function statusClass(status) {
    const slug = String(status || "not measured").toLowerCase().replace(/\s+/g, "-");
    return `di-status di-status-${slug}`;
  }

  function statusBadge(status) {
    if (!status) return "";
    return `<span class="${statusClass(status)}">${escapeHtml(status)}</span>`;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function heatColor(score) {
    if (score === null || score === undefined) {
      return { bg: "#f8f8f8", fg: "#4b5563", border: "#d1d5db" };
    }
    const s = Math.max(0, Math.min(100, Number(score) || 0));
    if (s >= 65) return { bg: "#dbeafe", fg: "#1e3a8a", border: "#93c5fd" };
    if (s >= 50) return { bg: "#e0f2fe", fg: "#075985", border: "#bae6fd" };
    if (s >= 35) return { bg: "#f1f5f9", fg: "#0f172a", border: "#cbd5e1" };
    if (s >= 22) return { bg: "#fef9c3", fg: "#713f12", border: "#fde047" };
    return { bg: "#fee2e2", fg: "#7f1d1d", border: "#fecaca" };
  }

  function popData() {
    return DATA.populations[currentPop];
  }

  function pillarOf(popId, pillarId) {
    const pop = DATA.populations[popId];
    return (pop.pillars || []).find((p) => p.id === pillarId) || {};
  }

  function bindAll() {
    document.querySelectorAll("[data-bind]").forEach((el) => {
      const path = el.getAttribute("data-bind");
      let value = getPath(DATA, path);
      const places = el.getAttribute("data-round");
      if (places !== null) {
        const formatted = formatNumber(value, places);
        el.textContent = formatted;
      } else if (value === null || value === undefined || value === "") {
        return;
      } else {
        el.textContent = String(value);
      }
    });
    document.querySelectorAll("[data-status]").forEach((el) => {
      const status = getPath(DATA, el.getAttribute("data-status"));
      if (!status) return;
      el.className = statusClass(status);
      el.textContent = status;
    });
    const eu = getPath(DATA, "populations.EU27.headline.display");
    const q = DATA.quarter_label || DATA.reference_period || "";
    const og = document.querySelector('meta[property="og:title"]');
    if (og && eu !== undefined) {
      og.setAttribute("content", `AI Diffusion Index: ${eu}/100 (${q})`);
    }
  }

  function renderGap() {
    const el = document.getElementById("gap-chart");
    if (!el) return;
    const rows = [
      ["EU27", "EU27"],
      ["FI", "Finland"],
    ];
    el.innerHTML = rows
      .map(([id, label]) => {
        const cap = pillarOf(id, "capital_intensity");
        const dep = pillarOf(id, "deployment");
        const bars = [
          ["Money committed", cap.score, cap.status, "capital"],
          ["Companies using AI", dep.score, dep.status, "use"],
        ];
        const barHtml = bars
          .map(([name, score, status]) => {
            const width = score === null || score === undefined ? 0 : Math.max(0, Math.min(100, score));
            return `<div class="di-gap-row">
              <div>${escapeHtml(name)} ${statusBadge(status)}</div>
              <div class="di-gap-track" aria-hidden="true"><div class="di-gap-fill" style="width:${width}%"></div></div>
              <div class="di-gap-val">${score === null || score === undefined ? "—" : formatNumber(score, 1)}</div>
            </div>`;
          })
          .join("");
        return `<div class="di-gap-group">
          <h3>${escapeHtml(label)}</h3>
          ${barHtml}
        </div>`;
      })
      .join("");
    el.setAttribute(
      "role",
      "img"
    );
    const euC = pillarOf("EU27", "capital_intensity").score;
    const euD = pillarOf("EU27", "deployment").score;
    const fiC = pillarOf("FI", "capital_intensity").score;
    const fiD = pillarOf("FI", "deployment").score;
    el.setAttribute(
      "aria-label",
      `Bar chart. EU27 money committed ${formatNumber(euC, 1)}, companies using AI ${formatNumber(euD, 1)}. Finland money committed ${formatNumber(fiC, 1)}, companies using AI ${formatNumber(fiD, 1)}, out of 100.`
    );
  }

  function renderScale() {
    const eu = getPath(DATA, "populations.EU27.headline.display");
    const fi = getPath(DATA, "populations.FI.headline.display");
    const pinEu = document.getElementById("pin-eu27");
    const pinFi = document.getElementById("pin-fi");
    const cap = document.getElementById("scale-pin-caption");
    if (pinEu && eu !== undefined) pinEu.style.left = `${Number(eu)}%`;
    if (pinFi && fi !== undefined) pinFi.style.left = `${Number(fi)}%`;
    if (cap) {
      cap.textContent = `Markers: EU27 ${eu}/100 and Finland ${fi}/100, ${DATA.quarter_label || ""}.`;
    }
  }

  function renderKPIs() {
    const pop = popData();
    const h = pop.headline;
    const dai = pop.dai || {};
    const pai = pop.pai || {};
    const gaps = pop.sector_gaps || [];
    const gap = gaps[0];
    const grid = document.getElementById("kpi-grid");
    if (!grid) return;
    const range = `${DATA.range_level} range ${formatNumber(h.p2_5, 0)}–${formatNumber(h.p97_5, 0)}`;
    const gapHtml = gap
      ? `<div class="di-kpi-card">
          <div>
            <div class="di-kpi-kicker">Industry gap · ${escapeHtml(PILLAR_LABELS[gap.pillar_id] || gap.pillar_id)}</div>
            <div class="di-kpi-val">${formatNumber(gap.gap_points, 1)}</div>
            <div class="di-kpi-band">points between ${escapeHtml(SECTOR_LABELS[gap.leader_sector_id] || gap.leader_sector_id)} (${formatNumber(gap.leader_score, 1)}, ${escapeHtml(gap.leader_grade || "")}) and ${escapeHtml(SECTOR_LABELS[gap.laggard_sector_id] || gap.laggard_sector_id)} (${formatNumber(gap.laggard_score, 1)}, ${escapeHtml(gap.laggard_grade || "")}).</div>
          </div>
        </div>`
      : `<div class="di-kpi-card">
          <div>
            <div class="di-kpi-kicker">Industry gap</div>
            <div class="di-kpi-val">—</div>
            <div class="di-kpi-band">${statusBadge("not measured")} No sector gap is published for this population yet.</div>
          </div>
        </div>`;
    grid.innerHTML = `
      <div class="di-kpi-card di-kpi-primary">
        <div>
          <div class="di-kpi-kicker">Headline · ${escapeHtml(POP_LABELS[currentPop])}</div>
          <div class="di-kpi-val">${escapeHtml(String(h.display ?? formatNumber(h.score, 0)))} <span style="font-size:15px;font-weight:400;color:var(--muted)">/ 100</span></div>
          <div class="di-kpi-band">${escapeHtml(range)} · median ${formatNumber(h.median, 1)} ${statusBadge(h.status)}</div>
        </div>
        <div class="di-kpi-foot">Combines only the measured headline pillars: company adoption and capital commitments, equally weighted. Reliable task completion is experimental and stays out of this number.</div>
      </div>
      <div class="di-kpi-card">
        <div>
          <div class="di-kpi-kicker">Digital AI (DAI)</div>
          <div class="di-kpi-val">${dai.score === null || dai.score === undefined ? "—" : formatNumber(dai.score, 1)}</div>
          <div class="di-kpi-band">${DATA.range_level} ${formatNumber(dai.p2_5, 1)}–${formatNumber(dai.p97_5, 1)} ${statusBadge(dai.status)}${dai.proxy ? " · proxy mix" : ""}</div>
        </div>
      </div>
      <div class="di-kpi-card">
        <div>
          <div class="di-kpi-kicker">Physical AI (PAI)</div>
          <div class="di-kpi-val">${pai.score === null || pai.score === undefined ? "—" : formatNumber(pai.score, 1)}</div>
          <div class="di-kpi-band">${DATA.range_level} ${formatNumber(pai.p2_5, 1)}–${formatNumber(pai.p97_5, 1)} ${statusBadge(pai.status)}</div>
        </div>
      </div>
      ${gapHtml}`;
  }

  function renderBlocks() {
    const el = document.getElementById("blocks-row");
    if (!el) return;
    const pop = popData();
    const boxes = [
      ["A. Diffusion proper (headline)", "The headline uses only pillars that meet the evidence rules.", BLOCKS.A],
      ["B. Conditions", "Published beside the headline, never blended into it.", BLOCKS.B],
      ["C. Consequences and distribution", "Published beside the headline, never blended into it.", BLOCKS.C],
    ];
    el.innerHTML = boxes
      .map(([title, note, ids]) => {
        const pills = ids
          .map((id) => {
            const p = (pop.pillars || []).find((x) => x.id === id) || { id, status: "not measured" };
            const score = p.score === null || p.score === undefined ? "—" : formatNumber(p.score, 1);
            return `<span class="di-badge">${escapeHtml(PILLAR_LABELS[id] || id)} · ${score} ${statusBadge(p.status)}</span>`;
          })
          .join(" ");
        return `<div class="di-block-box"><h3>${escapeHtml(title)}</h3><p>${escapeHtml(note)}</p><div class="di-pill-list">${pills}</div></div>`;
      })
      .join("");
  }

  function renderPaces() {
    const el = document.getElementById("pace-panel");
    if (!el) return;
    const paces = popData().paces || [];
    if (!paces.length) {
      el.innerHTML = `<p class="di-muted">No headline speed is published. A pace needs at least three comparable points in the same series segment and inside the 36-month window. See the <a href="diffusion-method.html">methodology</a>.</p>`;
      return;
    }
    const rows = paces
      .map((p) => {
        const sign = p.slope > 0 ? "+" : "";
        return `<tr>
          <th scope="row">${escapeHtml(PILLAR_LABELS[p.pillar_id] || p.pillar_id)} · ${escapeHtml(p.indicator_id)} (${escapeHtml(p.segment_id || "")})</th>
          <td>${sign}${formatNumber(p.slope, 1)} points a year (${formatNumber(p.p2_5, 1)} to ${formatNumber(p.p97_5, 1)})</td>
          <td>${escapeHtml(p.wording || "")} · ${escapeHtml((p.periods || []).join(", "))} · n=${escapeHtml(String(p.n_points))}</td>
        </tr>`;
      })
      .join("");
    el.innerHTML = `<h3>Published paces for ${escapeHtml(POP_LABELS[currentPop])}</h3>
      <p>These are indicator paces, not a single headline speed. A headline speed is not published in 1.0.0 because the headline series does not yet have three comparable points at the index level.</p>
      <div class="table-scroll"><table class="di-table">
        <thead><tr><th scope="col">Series</th><th scope="col">Pace</th><th scope="col">Reading</th></tr></thead>
        <tbody>${rows}</tbody>
      </table></div>`;
  }

  function cellKey(sectorId, pillarId) {
    return `${sectorId}::${pillarId}`;
  }

  function renderMatrix() {
    const thead = document.getElementById("matrix-thead");
    const tbody = document.getElementById("matrix-tbody");
    if (!thead || !tbody) return;
    const cells = {};
    (popData().grid_cells || []).forEach((c) => {
      cells[cellKey(c.sector_id, c.pillar_id)] = c;
    });
    thead.innerHTML = `<tr><th scope="col">Industry</th>${PILLAR_ORDER.map((id, i) => `<th scope="col" title="${escapeHtml(PILLAR_LABELS[id])}">P${i + 1}</th>`).join("")}</tr>`;
    tbody.innerHTML = SECTOR_ORDER.map((sectorId) => {
      const tds = PILLAR_ORDER.map((pillarId) => {
        const cell = cells[cellKey(sectorId, pillarId)] || { status: "not measured", score: null };
        const scored = cell.status === "scored" && cell.score !== null && cell.score !== undefined;
        const color = heatColor(scored ? cell.score : null);
        const label = scored ? formatNumber(cell.score, 1) : "—";
        const title = `${SECTOR_LABELS[sectorId]} · ${PILLAR_LABELS[pillarId]} · ${cell.status}${scored ? ` · ${formatNumber(cell.score, 1)}` : ""}`;
        const btn = scored
          ? `<button type="button" class="di-cell-btn" data-sector="${escapeHtml(sectorId)}" data-pillar="${escapeHtml(pillarId)}" style="background:${color.bg};color:${color.fg};border:1px solid ${color.border}" aria-label="${escapeHtml(title)}">${label}</button>`
          : `<span class="di-muted" title="${escapeHtml(title)}">${label}<span class="visually-hidden">, ${escapeHtml(cell.status)}</span></span>`;
        return `<td>${btn}</td>`;
      }).join("");
      return `<tr><th scope="row">${escapeHtml(SECTOR_LABELS[sectorId])}</th>${tds}</tr>`;
    }).join("");
    tbody.querySelectorAll(".di-cell-btn").forEach((btn) => {
      btn.addEventListener("click", () => openCellModal(btn.dataset.sector, btn.dataset.pillar));
    });
  }

  function openCellModal(sectorId, pillarId) {
    const cell = (popData().grid_cells || []).find((c) => c.sector_id === sectorId && c.pillar_id === pillarId);
    const modal = document.getElementById("cell-modal");
    if (!cell || !modal) return;
    document.getElementById("modal-kicker").textContent = `${POP_LABELS[currentPop]} · ${PILLAR_LABELS[pillarId] || pillarId}`;
    document.getElementById("modal-title").textContent = SECTOR_LABELS[sectorId] || sectorId;
    const score = cell.score === null || cell.score === undefined ? "—" : formatNumber(cell.score, 1);
    document.getElementById("modal-body").innerHTML = `
      <p><strong>${score}/100</strong> ${statusBadge(cell.status)} ${cell.grade ? `· grade ${escapeHtml(cell.grade)}` : ""}</p>
      <p>Coverage ${escapeHtml(cell.coverage || "—")} · observations: ${(cell.obs_ids || []).map((id) => escapeHtml(id)).join(", ") || "none"}.</p>
      ${cell.clipped ? "<p>This value was clipped to the 0–100 scale.</p>" : ""}
    `;
    if (typeof modal.showModal === "function") modal.showModal();
  }

  function renderPillars() {
    const grid = document.getElementById("pillar-grid");
    if (!grid) return;
    grid.innerHTML = (popData().pillars || [])
      .map((p) => {
        const score = p.score === null || p.score === undefined ? "—" : formatNumber(p.score, 1);
        const interval = p.interval
          ? `${DATA.range_level} ${formatNumber(p.interval.p2_5, 1)}–${formatNumber(p.interval.p97_5, 1)}`
          : "";
        return `<article class="di-pillar-card" id="pillar-card-${escapeHtml(p.id)}">
          <div class="di-pillar-head">
            <h3 class="di-pillar-title">${escapeHtml(PILLAR_LABELS[p.id] || p.id)}</h3>
            <div class="di-pillar-score">${score}</div>
          </div>
          <p>${statusBadge(p.status)} ${p.grade ? `· grade ${escapeHtml(p.grade)}` : ""} ${p.coverage ? `· coverage ${escapeHtml(p.coverage)}` : ""} · n=${escapeHtml(String(p.n ?? 0))}</p>
          ${interval ? `<p class="di-muted">${escapeHtml(interval)}</p>` : ""}
        </article>`;
      })
      .join("");
  }

  function renderBriefs() {
    const tbody = document.getElementById("briefs-signal-tbody");
    if (!tbody) return;
    const rows = DATA.brief_signals || [];
    tbody.innerHTML = rows
      .map((b) => {
        const href = `briefs/${b.brief_date}.html`;
        const title = b.title_en || b.title || b.brief_date;
        return `<tr>
          <th scope="row">${escapeHtml(b.brief_date)}</th>
          <td><a href="${escapeHtml(href)}">${escapeHtml(title)}</a></td>
          <td>${escapeHtml(PILLAR_LABELS[b.pillar] || b.pillar || "")}</td>
          <td>${escapeHtml(SECTOR_LABELS[b.sector] || b.sector || "")}</td>
        </tr>`;
      })
      .join("");
  }

  function renderPlanetary() {
    const panel = document.getElementById("pb-ecometer-panel");
    const tbody = document.getElementById("pb-tbody");
    const pb = DATA.planetary_boundaries || {};
    const meter = pb.summary_meter || {};
    if (panel) {
      const rule = meter.headline_rule_en || pb.framework || "";
      panel.innerHTML = `<p>${escapeHtml(rule)}</p>
        <p>Reference status: ${escapeHtml(String(pb.transgressed_count ?? "—"))} planetary boundaries are assessed as transgressed. This is not an index score. ${statusBadge("not measured") } for an AI-specific net figure.</p>`;
    }
    if (!tbody) return;
    tbody.innerHTML = (pb.boundaries || [])
      .map((b) => `<tr>
        <th scope="row">${escapeHtml(b.name_en || b.id)}</th>
        <td>${escapeHtml(b.status_code || "")} ${b.ai_measured ? "" : statusBadge("not measured")}</td>
        <td>${b.burden_score === null || b.burden_score === undefined ? "—" : formatNumber(b.burden_score, 1)} · ${escapeHtml(b.burden_status || "")}</td>
        <td>${b.abatement_score === null || b.abatement_score === undefined ? "—" : formatNumber(b.abatement_score, 1)} · ${escapeHtml(b.abatement_status || "")}</td>
      </tr>`)
      .join("");
  }

  function parseCsv(text) {
    const rows = [];
    let row = [];
    let cell = "";
    let inQuotes = false;
    for (let i = 0; i < text.length; i += 1) {
      const ch = text[i];
      if (inQuotes) {
        if (ch === '"' && text[i + 1] === '"') {
          cell += '"';
          i += 1;
        } else if (ch === '"') {
          inQuotes = false;
        } else {
          cell += ch;
        }
      } else if (ch === '"') {
        inQuotes = true;
      } else if (ch === ",") {
        row.push(cell);
        cell = "";
      } else if (ch === "\n") {
        row.push(cell);
        rows.push(row);
        row = [];
        cell = "";
      } else if (ch !== "\r") {
        cell += ch;
      }
    }
    if (cell.length || row.length) {
      row.push(cell);
      rows.push(row);
    }
    if (!rows.length) return [];
    const header = rows[0];
    return rows.slice(1).filter((r) => r.length && r.some((c) => c !== "")).map((r) => {
      const obj = {};
      header.forEach((key, idx) => {
        obj[key] = r[idx] ?? "";
      });
      return obj;
    });
  }

  function observationStatus(row) {
    const stale = new Set(DATA.stale_observations || []);
    if (stale.has(row.obs_id)) return "stale";
    if (String(row.trust_tier) === "5") return "incomplete";
    if (!row.indicator_id) return "not measured";
    return "scored";
  }

  function renderObservations() {
    const tbody = document.getElementById("obs-tbody");
    const count = document.getElementById("obs-count");
    if (count) count.textContent = String(SERIES.length);
    if (!tbody) return;
    tbody.innerHTML = SERIES.map((row) => {
      const status = observationStatus(row);
      return `<tr>
        <th scope="row">${escapeHtml(row.obs_id)}</th>
        <td>${escapeHtml(row.period)}</td>
        <td>${escapeHtml(row.geo)}</td>
        <td>${escapeHtml(row.indicator_id || "—")}</td>
        <td>${escapeHtml(row.value)} ${escapeHtml(row.unit || "")}</td>
        <td>${statusBadge(status)}</td>
      </tr>`;
    }).join("");
  }

  function renderSources() {
    const tbody = document.getElementById("sources-tbody");
    if (!tbody) return;
    tbody.innerHTML = (DATA.sources || [])
      .map((s) => {
        const flag = s.verified ? '<span class="di-badge di-badge-verified">[V] checked</span>' : '<span class="di-badge di-badge-candidate">[K] candidate</span>';
        const name = s.url ? `<a href="${escapeHtml(s.url)}">${escapeHtml(s.name || s.id)}</a>` : escapeHtml(s.name || s.id);
        const pillars = (s.pillars || []).map((id) => PILLAR_LABELS[id] || id).join(", ");
        return `<tr><th scope="row">${name}</th><td>${flag}</td><td>${escapeHtml(pillars)}</td></tr>`;
      })
      .join("");
  }

  function renderDashboard() {
    renderKPIs();
    renderBlocks();
    renderPaces();
    renderMatrix();
    renderPillars();
  }

  function renderAll() {
    bindAll();
    renderGap();
    renderScale();
    renderDashboard();
    renderBriefs();
    renderPlanetary();
    renderObservations();
    renderSources();
  }

  function setPopulation(pop) {
    if (!DATA.populations[pop]) return;
    currentPop = pop;
    document.querySelectorAll(".di-pop-toggle [data-pop]").forEach((btn) => {
      btn.setAttribute("aria-pressed", btn.dataset.pop === pop ? "true" : "false");
    });
    const url = new URL(window.location.href);
    if (pop === "EU27") url.searchParams.delete("pop");
    else url.searchParams.set("pop", pop);
    history.replaceState({}, "", url);
    renderDashboard();
  }

  document.querySelectorAll(".di-pop-toggle [data-pop]").forEach((btn) => {
    btn.addEventListener("click", () => setPopulation(btn.dataset.pop));
  });

  const params = new URLSearchParams(window.location.search);
  if (params.get("pop") === "FI") currentPop = "FI";

  Promise.all([
    fetch(COMPUTED_URL).then((r) => {
      if (!r.ok) throw new Error(`Failed to load ${COMPUTED_URL}`);
      return r.json();
    }),
    fetch(SERIES_URL).then((r) => (r.ok ? r.text() : "")),
  ])
    .then(([computed, csvText]) => {
      DATA = computed;
      SERIES = csvText ? parseCsv(csvText) : [];
      document.querySelectorAll(".di-pop-toggle [data-pop]").forEach((btn) => {
        btn.setAttribute("aria-pressed", btn.dataset.pop === currentPop ? "true" : "false");
      });
      renderAll();
    })
    .catch((err) => {
      console.error(err);
      const main = document.getElementById("main-content");
      if (main) {
        const warn = document.createElement("p");
        warn.className = "di-js-required";
        warn.textContent = "The live scores could not be loaded. The placeholders below are not publication figures. See the methodology page for the data files.";
        main.prepend(warn);
      }
    });
})();
