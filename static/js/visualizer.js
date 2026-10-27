/**
 * Visualizer Rendering Engine
 * Handles rendering of:
 * 1. Array Bars (Merge Sort, Quick Sort, Binary Search, Kadane)
 * 2. Recursion Trees (Merge Sort, Huffman Coding)
 * 3. 2D/1D DP Tables (0/1 Knapsack, LCS, Coin Change, MCM, Fibonacci)
 * 4. Weighted Graph Canvas (Dijkstra)
 * 5. Gantt & Timeline Slots (Activity Selection, Job Sequencing)
 * 6. Fractional Knapsack Capacity Meter
 */

class VisualizerRenderer {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
  }

  clear() {
    if (this.container) this.container.innerHTML = "";
  }

  /**
   * 1. Render Array Bars
   */
  renderArrayBars(state, algorithm) {
    this.clear();
    const arr = state.array || [];
    if (!arr.length) return;

    const maxVal = Math.max(...arr.map(v => Math.abs(v)), 1);
    const wrapper = document.createElement("div");
    wrapper.className = "array-bars-container";

    const comparing = new Set(state.comparing || []);
    const swapped = new Set(state.swapped || []);
    const sorted = new Set(state.sorted_indices || state.merged || []);
    const eliminated = new Set([...(state.eliminated_left || []), ...(state.eliminated_right || [])]);

    const low = state.low !== undefined ? state.low : -1;
    const high = state.high !== undefined ? state.high : -1;
    const mid = state.mid !== undefined ? state.mid : -1;
    const pivot = state.pivot_index !== undefined ? state.pivot_index : -1;

    // Window bounds for Kadane
    const window = state.current_window || [];
    const bestWindow = state.best_window || [];

    arr.forEach((val, idx) => {
      const col = document.createElement("div");
      col.className = "bar-column";

      // Pointer tags
      const pointerTags = [];
      if (idx === pivot) pointerTags.push({ label: "PIVOT", class: "tag-pivot" });
      if (idx === low && low === high) pointerTags.push({ label: "L,H", class: "tag-pointer" });
      else {
        if (idx === low) pointerTags.push({ label: "LOW", class: "tag-pointer" });
        if (idx === high) pointerTags.push({ label: "HIGH", class: "tag-pointer" });
      }
      if (idx === mid) pointerTags.push({ label: "MID", class: "tag-mid" });
      if (state.pointer_i === idx) pointerTags.push({ label: "i", class: "tag-sub" });
      if (state.pointer_j === idx) pointerTags.push({ label: "j", class: "tag-sub" });

      const tagContainer = document.createElement("div");
      tagContainer.className = "bar-tags";
      pointerTags.forEach(t => {
        const span = document.createElement("span");
        span.className = `badge-tag ${t.class}`;
        span.textContent = t.label;
        tagContainer.appendChild(span);
      });
      col.appendChild(tagContainer);

      // Bar element
      const bar = document.createElement("div");
      bar.className = "bar-element";

      // Determine bar status class
      if (idx === pivot) bar.classList.add("bar-pivot");
      else if (comparing.has(idx)) bar.classList.add("bar-comparing");
      else if (swapped.has(idx)) bar.classList.add("bar-swapped");
      else if (sorted.has(idx)) bar.classList.add("bar-sorted");
      else if (idx === mid) bar.classList.add("bar-mid");
      else if (eliminated.has(idx)) bar.classList.add("bar-eliminated");

      // Kadane window highlight
      if (window.length === 2 && idx >= window[0] && idx <= window[1]) {
        bar.classList.add("bar-in-window");
      }

      // Height calculation
      const barHeightPct = Math.max(12, Math.min(94, Math.round((Math.abs(val) / maxVal) * 88)));
      bar.style.height = `${barHeightPct}%`;

      const valLabel = document.createElement("span");
      valLabel.className = "bar-value";
      valLabel.textContent = val;
      bar.appendChild(valLabel);

      col.appendChild(bar);

      // Index label
      const idxLabel = document.createElement("div");
      idxLabel.className = "bar-index";
      idxLabel.textContent = `[${idx}]`;
      col.appendChild(idxLabel);

      wrapper.appendChild(col);
    });

    this.container.appendChild(wrapper);
  }

  /**
   * 2. Render 2D DP Table (0/1 Knapsack, LCS, MCM)
   */
  renderDPTable(state, algorithm) {
    this.clear();
    const table = state.dp_table || state.m_table || [];
    if (!table.length) return;

    const wrapper = document.createElement("div");
    wrapper.className = "dp-table-wrapper";

    const currentCell = state.current_cell || [-1, -1];
    const refCells = new Set((state.reference_cells || []).map(c => `${c[0]},${c[1]}`));
    const backtrackPath = new Set((state.backtrack_path || []).map(c => `${c[0]},${c[1]}`));

    const htmlTable = document.createElement("table");
    htmlTable.className = "dp-grid";

    // Header row
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    
    // Top-left blank corner
    const cornerTh = document.createElement("th");
    cornerTh.textContent = algorithm.includes("LCS") ? "S1 \\ S2" : "Item \\ Cap";
    headerRow.appendChild(cornerTh);

    const cols = table[0].length;
    for (let c = 0; c < cols; c++) {
      const th = document.createElement("th");
      if (algorithm.includes("LCS")) {
        th.textContent = c === 0 ? "ε" : state.s2 ? state.s2[c - 1] : c;
      } else if (algorithm.includes("MCM")) {
        th.textContent = `j=${c}`;
      } else {
        th.textContent = `w=${c}`;
      }
      headerRow.appendChild(th);
    }
    thead.appendChild(headerRow);
    htmlTable.appendChild(thead);

    // Body rows
    const tbody = document.createElement("tbody");
    table.forEach((row, r) => {
      const tr = document.createElement("tr");
      const rowTh = document.createElement("th");
      if (algorithm.includes("LCS")) {
        rowTh.textContent = r === 0 ? "ε" : state.s1 ? state.s1[r - 1] : r;
      } else if (algorithm.includes("MCM")) {
        rowTh.textContent = `i=${r}`;
      } else {
        if (r === 0) rowTh.textContent = "0";
        else {
          const item = state.items ? state.items[r - 1] : null;
          rowTh.textContent = item ? `I${r} (w:${item.weight}, v:${item.value})` : `i=${r}`;
        }
      }
      tr.appendChild(rowTh);

      row.forEach((cellVal, c) => {
        const td = document.createElement("td");
        const cellCoord = `${r},${c}`;
        td.className = "dp-cell";

        if (r === currentCell[0] && c === currentCell[1]) {
          td.classList.add("cell-active");
        } else if (refCells.has(cellCoord)) {
          td.classList.add("cell-referenced");
        } else if (backtrackPath.has(cellCoord)) {
          td.classList.add("cell-backtrack");
        }

        td.textContent = cellVal === 999999 || cellVal === Infinity ? "∞" : cellVal;
        td.title = `Cell [${r}, ${c}] = ${cellVal}`;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });

    htmlTable.appendChild(tbody);
    wrapper.appendChild(htmlTable);

    // Formula Callout Card if formula exists
    if (state.formula) {
      const formulaCard = document.createElement("div");
      formulaCard.className = "formula-card";
      formulaCard.innerHTML = `<span class="formula-icon">📐</span> <span class="formula-text">${state.formula}</span>`;
      wrapper.appendChild(formulaCard);
    }

    this.container.appendChild(wrapper);
  }

  /**
   * 3. Render 1D DP Array (Coin Change, Fibonacci)
   */
  render1DArray(state, algorithm) {
    this.clear();
    const arr = state.dp_array || [];
    if (!arr.length) return;

    const wrapper = document.createElement("div");
    wrapper.className = "dp-1d-wrapper";

    const currIdx = state.current_amount !== undefined ? state.current_amount : state.current_index;
    const refIdx = state.referenced_amount !== undefined ? state.referenced_amount : (state.referenced_indices || []);
    const refSet = new Set(Array.isArray(refIdx) ? refIdx : [refIdx]);

    const strip = document.createElement("div");
    strip.className = "dp-1d-strip";

    arr.forEach((val, idx) => {
      const cell = document.createElement("div");
      cell.className = "dp-1d-cell";

      if (idx === currIdx) cell.classList.add("cell-active");
      else if (refSet.has(idx)) cell.classList.add("cell-referenced");

      const idxDiv = document.createElement("div");
      idxDiv.className = "dp-1d-idx";
      idxDiv.textContent = algorithm.includes("Coin") ? `Amt ${idx}` : `F(${idx})`;

      const valDiv = document.createElement("div");
      valDiv.className = "dp-1d-val";
      valDiv.textContent = val;

      cell.appendChild(idxDiv);
      cell.appendChild(valDiv);
      strip.appendChild(cell);
    });

    wrapper.appendChild(strip);

    if (state.formula) {
      const formulaCard = document.createElement("div");
      formulaCard.className = "formula-card";
      formulaCard.innerHTML = `<span class="formula-icon">📐</span> <span class="formula-text">${state.formula}</span>`;
      wrapper.appendChild(formulaCard);
    }

    if (state.backtrack_coins && state.backtrack_coins.length) {
      const coinsCard = document.createElement("div");
      coinsCard.className = "coins-solution-card";
      coinsCard.innerHTML = `
        <span class="solution-badge">Optimal Coins:</span>
        ${state.backtrack_coins.map(c => `<span class="coin-pill">🪙 ${c}</span>`).join(" + ")} = ${state.amount}
      `;
      wrapper.appendChild(coinsCard);
    }

    this.container.appendChild(wrapper);
  }

  /**
   * 4. Render Fractional Knapsack Capacity Meter & Items Table
   */
  renderFractionalKnapsack(state) {
    this.clear();
    const items = state.items || [];
    const capacity = state.capacity || 1;
    const usedCap = state.used_capacity || 0;
    const totalVal = state.total_value || 0;
    const percent = Math.min(100, Math.round((usedCap / capacity) * 100));

    const wrapper = document.createElement("div");
    wrapper.className = "knapsack-visual-wrapper";

    // Bag Container Meter
    const bagCard = document.createElement("div");
    bagCard.className = "knapsack-bag-card";
    bagCard.innerHTML = `
      <div class="bag-header">
        <div class="bag-title">🎒 Knapsack Bag Fill Level</div>
        <div class="bag-metrics">
          <span>Capacity: <strong>${usedCap} / ${capacity}</strong> kg</span>
          <span class="highlight-val">Total Value: <strong>$${totalVal}</strong></span>
        </div>
      </div>
      <div class="liquid-meter-track">
        <div class="liquid-meter-fill" style="width: ${percent}%;">
          <span class="meter-text">${percent}% Full</span>
        </div>
      </div>
    `;
    wrapper.appendChild(bagCard);

    // Items Table
    const tableCard = document.createElement("div");
    tableCard.className = "items-table-card";
    tableCard.innerHTML = `
      <table class="knapsack-items-grid">
        <thead>
          <tr>
            <th>Item</th>
            <th>Weight</th>
            <th>Value</th>
            <th>Ratio (v/w)</th>
            <th>Status</th>
            <th>Fraction Taken</th>
          </tr>
        </thead>
        <tbody>
          ${items.map(it => {
            let statusBadge = `<span class="badge-status status-unprocessed">Waiting</span>`;
            if (it.status === "inspecting") statusBadge = `<span class="badge-status status-inspecting">Inspecting</span>`;
            else if (it.status === "taken_full") statusBadge = `<span class="badge-status status-full">100% Taken</span>`;
            else if (it.status === "taken_fraction") statusBadge = `<span class="badge-status status-fraction">Partial (${Math.round(it.fraction_taken * 100)}%)</span>`;
            else if (it.status === "rejected") statusBadge = `<span class="badge-status status-rejected">Skipped</span>`;

            return `
              <tr class="${it.status}">
                <td><strong>${it.name}</strong></td>
                <td>${it.weight} kg</td>
                <td>$${it.value}</td>
                <td><span class="ratio-pill">${it.ratio}</span></td>
                <td>${statusBadge}</td>
                <td><strong class="frac-val">${(it.fraction_taken * 100).toFixed(1)}%</strong></td>
              </tr>
            `;
          }).join("")}
        </tbody>
      </table>
    `;
    wrapper.appendChild(tableCard);

    this.container.appendChild(wrapper);
  }

  /**
   * 5. Render Weighted Graph for Dijkstra
   */
  renderGraph(state) {
    this.clear();
    const nodes = state.nodes || [];
    const edges = state.edges || [];
    const distances = state.distances || {};
    const visited = new Set(state.visited || []);
    const currNode = state.current_node;
    const activeEdge = state.active_edge;
    const relaxedEdge = state.relaxed_edge;

    const wrapper = document.createElement("div");
    wrapper.className = "graph-visual-wrapper";

    // SVG Canvas
    const svgWidth = 620;
    const svgHeight = 360;
    const radius = 135;
    const centerX = svgWidth / 2;
    const centerY = svgHeight / 2;

    // Layout nodes in polygon circle
    const nodeCoords = {};
    nodes.forEach((n, i) => {
      const angle = (2 * Math.PI * i) / nodes.length - Math.PI / 2;
      nodeCoords[n] = {
        x: Math.round(centerX + radius * Math.cos(angle)),
        y: Math.round(centerY + radius * Math.sin(angle))
      };
    });

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", `0 0 ${svgWidth} ${svgHeight}`);
    svg.setAttribute("class", "graph-svg");

    // Defs for arrows/glows
    svg.innerHTML = `
      <defs>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="3" result="glow" />
          <feComposite in="SourceGraphic" in2="glow" operator="over" />
        </filter>
      </defs>
    `;

    // Draw Edges
    edges.forEach(e => {
      const p1 = nodeCoords[e.from];
      const p2 = nodeCoords[e.to];
      if (!p1 || !p2) return;

      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", p1.x);
      line.setAttribute("y1", p1.y);
      line.setAttribute("x2", p2.x);
      line.setAttribute("y2", p2.y);
      line.setAttribute("class", "graph-edge");

      if (relaxedEdge && ((relaxedEdge.from === e.from && relaxedEdge.to === e.to) || (relaxedEdge.from === e.to && relaxedEdge.to === e.from))) {
        line.setAttribute("class", "graph-edge edge-relaxed");
      } else if (activeEdge && ((activeEdge.from === e.from && activeEdge.to === e.to) || (activeEdge.from === e.to && activeEdge.to === e.from))) {
        line.setAttribute("class", "graph-edge edge-active");
      }

      svg.appendChild(line);

      // Edge weight label
      const midX = (p1.x + p2.x) / 2;
      const midY = (p1.y + p2.y) / 2;
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", midX);
      text.setAttribute("y", midY - 6);
      text.setAttribute("class", "edge-label");
      text.textContent = e.weight;
      svg.appendChild(text);
    });

    // Draw Nodes
    nodes.forEach(n => {
      const coord = nodeCoords[n];
      if (!coord) return;

      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("class", "graph-node-group");

      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", coord.x);
      circle.setAttribute("cy", coord.y);
      circle.setAttribute("r", 24);
      circle.setAttribute("class", "graph-node");

      if (n === currNode) circle.setAttribute("class", "graph-node node-current");
      else if (visited.has(n)) circle.setAttribute("class", "graph-node node-visited");

      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("x", coord.x);
      label.setAttribute("y", coord.y + 5);
      label.setAttribute("class", "node-label");
      label.textContent = n;

      g.appendChild(circle);
      g.appendChild(label);
      svg.appendChild(g);
    });

    wrapper.appendChild(svg);

    // Distance vector table
    const distPanel = document.createElement("div");
    distPanel.className = "dijkstra-distance-bar";
    distPanel.innerHTML = `
      <div class="dijkstra-dist-title">Shortest Distance Vector <code>dist[v]</code></div>
      <div class="dijkstra-dist-cards">
        ${nodes.map(n => {
          const d = distances[n];
          const isFinal = visited.has(n);
          return `
            <div class="dist-card ${isFinal ? 'finalized' : ''} ${n === currNode ? 'active' : ''}">
              <div class="dist-node-badge">${n}</div>
              <div class="dist-val">${d === "inf" ? '∞' : d}</div>
              <div class="dist-sub">${isFinal ? 'Finalized' : 'Provisional'}</div>
            </div>
          `;
        }).join("")}
      </div>
    `;
    wrapper.appendChild(distPanel);

    this.container.appendChild(wrapper);
  }

  /**
   * 6. Render Activity Selection Timeline
   */
  renderActivities(state) {
    this.clear();
    const acts = state.activities || [];
    const maxFinish = Math.max(...acts.map(a => a.finish), 12);
    const currIdx = state.current_activity_index;
    const selectedIds = new Set(state.selected_ids || []);

    const wrapper = document.createElement("div");
    wrapper.className = "activity-timeline-wrapper";

    // Timeline Ruler
    const ruler = document.createElement("div");
    ruler.className = "timeline-ruler";
    for (let t = 0; t <= maxFinish; t += 2) {
      const tick = document.createElement("div");
      tick.className = "timeline-tick";
      tick.style.left = `${(t / maxFinish) * 100}%`;
      tick.textContent = `${t}:00`;
      ruler.appendChild(tick);
    }
    wrapper.appendChild(ruler);

    // Bars
    acts.forEach((act, idx) => {
      const row = document.createElement("div");
      row.className = "activity-row";

      const leftPct = (act.start / maxFinish) * 100;
      const widthPct = ((act.finish - act.start) / maxFinish) * 100;

      const bar = document.createElement("div");
      bar.className = "activity-bar";
      bar.style.left = `${leftPct}%`;
      bar.style.width = `${widthPct}%`;

      if (act.status === "selected") bar.classList.add("act-selected");
      else if (act.status === "conflict") bar.classList.add("act-conflict");
      else if (act.status === "checking") bar.classList.add("act-checking");

      bar.innerHTML = `
        <span class="act-id"><strong>${act.id}</strong> [${act.start} -> ${act.finish}]</span>
        <span class="act-tag">${act.status.toUpperCase()}</span>
      `;

      row.appendChild(bar);
      wrapper.appendChild(row);
    });

    this.container.appendChild(wrapper);
  }

  /**
   * 7. Render Job Sequencing Slots
   */
  renderJobSequencing(state) {
    this.clear();
    const slots = state.slots || [];
    const jobs = state.jobs || [];
    const currJobIdx = state.current_job_index;
    const currSlot = state.checked_slot;

    const wrapper = document.createElement("div");
    wrapper.className = "jobs-wrapper";

    // Slots visual
    const slotsCard = document.createElement("div");
    slotsCard.className = "slots-container-card";
    slotsCard.innerHTML = `
      <div class="slots-header">📅 Schedule Timeline Slots</div>
      <div class="slots-strip">
        ${slots.map(s => `
          <div class="slot-box ${s.slot === currSlot ? 'slot-checking' : ''} ${s.job ? 'slot-occupied' : 'slot-free'}">
            <div class="slot-number">Slot ${s.slot}</div>
            <div class="slot-content">${s.job ? `✅ ${s.job}` : 'FREE'}</div>
          </div>
        `).join("")}
      </div>
    `;
    wrapper.appendChild(slotsCard);

    // Jobs sorted list
    const jobsCard = document.createElement("div");
    jobsCard.className = "jobs-list-card";
    jobsCard.innerHTML = `
      <table class="knapsack-items-grid">
        <thead>
          <tr>
            <th>Job</th>
            <th>Profit</th>
            <th>Deadline</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${jobs.map((j, idx) => `
            <tr class="${idx === currJobIdx ? 'inspecting' : ''} ${j.status}">
              <td><strong>${j.id}</strong></td>
              <td><span class="profit-pill">+$${j.profit}</span></td>
              <td>Deadline: Slot ${j.deadline}</td>
              <td><span class="badge-status status-${j.status}">${j.status.toUpperCase()}</span></td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    `;
    wrapper.appendChild(jobsCard);

    this.container.appendChild(wrapper);
  }

  /**
   * 8. Render Huffman Tree
   */
  renderHuffman(state) {
    this.clear();
    const allNodes = state.all_nodes || [];
    const pq = state.priority_queue || [];
    const merging = new Set(state.merging_nodes || []);

    const wrapper = document.createElement("div");
    wrapper.className = "huffman-wrapper";

    // Min-Queue Priority Strip
    const pqCard = document.createElement("div");
    pqCard.className = "huffman-pq-card";
    pqCard.innerHTML = `
      <div class="pq-header">Min-Priority Queue (Lowest Frequencies First)</div>
      <div class="huffman-pq-strip">
        ${pq.map(n => `
          <div class="huffman-chip ${merging.has(n.id) ? 'chip-merging' : ''}">
            <span class="chip-char">'${n.char}'</span>
            <span class="chip-freq">freq: ${n.freq}</span>
          </div>
        `).join("")}
      </div>
    `;
    wrapper.appendChild(pqCard);

    // Tree nodes diagram
    const treeCard = document.createElement("div");
    treeCard.className = "huffman-tree-card";
    treeCard.innerHTML = `
      <div class="pq-header">Formed Binary Subtrees & Prefix Encoded Nodes</div>
      <div class="huffman-nodes-grid">
        ${allNodes.map(n => `
          <div class="hnode ${n.is_leaf ? 'hnode-leaf' : 'hnode-internal'} ${merging.has(n.id) ? 'hnode-active' : ''}">
            <div class="hnode-label">${n.char}</div>
            <div class="hnode-freq">Weight: ${n.freq}</div>
            ${n.is_leaf ? '<span class="leaf-tag">LEAF</span>' : '<span class="branch-tag">BRANCH</span>'}
          </div>
        `).join("")}
      </div>
    `;
    wrapper.appendChild(treeCard);

    this.container.appendChild(wrapper);
  }

  /**
   * 9. Render Merge Sort Recursion Tree
   */
  renderRecursionTree(state) {
    const nodes = state.tree_nodes || [];
    if (!nodes.length) return;

    const treeContainer = document.getElementById("recursion-tree-view");
    if (!treeContainer) return;
    treeContainer.innerHTML = "";

    const activeNodeId = state.tree_node_id;
    const treeDiv = document.createElement("div");
    treeDiv.className = "tree-hierarchy";

    // Group nodes by depth
    const depthMap = {};
    nodes.forEach(n => {
      depthMap[n.depth] = depthMap[n.depth] || [];
      depthMap[n.depth].push(n);
    });

    Object.keys(depthMap).sort((a, b) => a - b).forEach(d => {
      const levelDiv = document.createElement("div");
      levelDiv.className = "tree-level";

      depthMap[d].forEach(n => {
        const nodeDiv = document.createElement("div");
        nodeDiv.className = `tree-node node-status-${n.status}`;
        if (n.id === activeNodeId) nodeDiv.classList.add("tree-node-active");

        nodeDiv.innerHTML = `
          <div class="tree-node-content">${n.label}</div>
          <div class="tree-node-badge">${n.status}</div>
        `;
        levelDiv.appendChild(nodeDiv);
      });

      treeDiv.appendChild(levelDiv);
    });

    treeContainer.appendChild(treeDiv);
  }
}
