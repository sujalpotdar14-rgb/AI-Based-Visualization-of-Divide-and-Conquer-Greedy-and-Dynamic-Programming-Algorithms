/**
 * Main Application Controller
 * Connects UI, Visualizer, AI Copilot, and Backend API
 */

class DAAApp {
  constructor() {
    this.currentParadigm = "divide_and_conquer";
    this.currentAlgorithm = "merge_sort";
    this.currentData = null;
    this.steps = [];
    this.currentStepIndex = 0;
    this.isPlaying = false;
    this.playTimer = null;
    this.playbackSpeed = 1000; // ms per step
    this.soundEnabled = true;

    this.renderer = new VisualizerRenderer("visualization-canvas");
    this.initAudio();
    this.initUI();
    this.bindEvents();
    this.loadAlgorithm(this.currentParadigm, this.currentAlgorithm);
  }

  initAudio() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioContext();
    } catch (e) {
      this.audioCtx = null;
    }
  }

  playTone(freq = 440, type = "sine", duration = 0.05) {
    if (!this.soundEnabled || !this.audioCtx) return;
    try {
      if (this.audioCtx.state === "suspended") this.audioCtx.resume();
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);
      gain.gain.setValueAtTime(0.04, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.audioCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start();
      osc.stop(this.audioCtx.currentTime + duration);
    } catch (e) {}
  }

  initUI() {
    // Populate API key input if stored
    const keyInput = document.getElementById("gemini-key-input");
    if (keyInput && window.aiCopilot.apiKey) {
      keyInput.value = window.aiCopilot.apiKey;
    }
  }

  bindEvents() {
    // Paradigm Navigation Tabs
    document.querySelectorAll(".paradigm-tab").forEach(tab => {
      tab.addEventListener("click", e => {
        const paradigm = tab.getAttribute("data-paradigm");
        this.switchParadigm(paradigm);
      });
    });

    // Algorithm Selector Pills
    document.querySelectorAll(".algo-pill").forEach(pill => {
      pill.addEventListener("click", e => {
        const algo = pill.getAttribute("data-algo");
        this.selectAlgorithm(algo);
      });
    });

    // Playback Controls
    const playBtn = document.getElementById("btn-play");
    if (playBtn) playBtn.addEventListener("click", () => this.togglePlay());

    const nextBtn = document.getElementById("btn-next");
    if (nextBtn) nextBtn.addEventListener("click", () => this.stepForward());

    const prevBtn = document.getElementById("btn-prev");
    if (prevBtn) prevBtn.addEventListener("click", () => this.stepBackward());

    const resetBtn = document.getElementById("btn-reset");
    if (resetBtn) resetBtn.addEventListener("click", () => this.resetVisualization());

    // Speed Slider
    const speedSlider = document.getElementById("speed-slider");
    if (speedSlider) {
      speedSlider.addEventListener("input", e => {
        const val = parseFloat(e.target.value);
        this.playbackSpeed = Math.round(1000 / val);
        const label = document.getElementById("speed-val");
        if (label) label.textContent = `${val}x`;
        if (this.isPlaying) {
          this.pause();
          this.play();
        }
      });
    }

    // Step Scrubber
    const scrubber = document.getElementById("step-scrubber");
    if (scrubber) {
      scrubber.addEventListener("input", e => {
        this.goToStep(parseInt(e.target.value, 10));
      });
    }

    // Keyboard Shortcuts
    window.addEventListener("keydown", e => {
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
      if (e.code === "Space") {
        e.preventDefault();
        this.togglePlay();
      } else if (e.code === "ArrowRight") {
        e.preventDefault();
        this.stepForward();
      } else if (e.code === "ArrowLeft") {
        e.preventDefault();
        this.stepBackward();
      } else if (e.code === "KeyR") {
        e.preventDefault();
        this.resetVisualization();
      }
    });

    // Run / Apply Custom Input Button
    const runBtn = document.getElementById("btn-apply-input");
    if (runBtn) {
      runBtn.addEventListener("click", () => this.runCustomInput());
    }

    // AI Generate Testcase Button
    const genBtn = document.getElementById("btn-ai-gen-testcase");
    if (genBtn) {
      genBtn.addEventListener("click", () => this.generateAITestcase());
    }

    // Inspector Tabs (AI Explanation, Pseudocode, Code, Metrics)
    document.querySelectorAll(".inspector-tab").forEach(tab => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".inspector-tab").forEach(t => t.classList.remove("active"));
        document.querySelectorAll(".inspector-panel").forEach(p => p.classList.remove("active"));
        tab.classList.add("active");
        const targetId = tab.getAttribute("data-target");
        const panel = document.getElementById(targetId);
        if (panel) panel.classList.add("active");
      });
    });

    // Code Language Selector
    document.querySelectorAll(".lang-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".lang-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        this.updateCodeSnippet(btn.getAttribute("data-lang"));
      });
    });

    // Sound toggle
    const soundBtn = document.getElementById("btn-sound-toggle");
    if (soundBtn) {
      soundBtn.addEventListener("click", () => {
        this.soundEnabled = !this.soundEnabled;
        soundBtn.innerHTML = this.soundEnabled ? "🔊 Sound ON" : "🔇 Sound OFF";
        soundBtn.classList.toggle("muted", !this.soundEnabled);
      });
    }

    // API Key Save
    const saveKeyBtn = document.getElementById("btn-save-key");
    if (saveKeyBtn) {
      saveKeyBtn.addEventListener("click", () => {
        const key = document.getElementById("gemini-key-input").value;
        window.aiCopilot.setApiKey(key);
        alert(key.trim() ? "Gemini API Key saved! AI Tutor will use Gemini 2.5." : "Using Built-in DAA Expert Engine.");
      });
    }

    // AI Problem Detective Form
    const analyzeBtn = document.getElementById("btn-detective-analyze");
    if (analyzeBtn) {
      analyzeBtn.addEventListener("click", () => this.runProblemDetective());
    }

    // Master Theorem Form
    const mtBtn = document.getElementById("btn-mt-calc");
    if (mtBtn) {
      mtBtn.addEventListener("click", () => this.runMasterTheorem());
    }
  }

  switchParadigm(paradigm) {
    this.currentParadigm = paradigm;
    document.querySelectorAll(".paradigm-tab").forEach(t => {
      t.classList.toggle("active", t.getAttribute("data-paradigm") === paradigm);
    });

    // Toggle main workspace vs special views (Detective, Master Theorem)
    const visualizerView = document.getElementById("visualizer-main-view");
    const detectiveView = document.getElementById("ai-detective-view");
    const mtView = document.getElementById("master-theorem-view");

    if (paradigm === "ai_detective") {
      visualizerView.style.display = "none";
      mtView.style.display = "none";
      detectiveView.style.display = "block";
      this.loadPresetProblems();
      return;
    } else if (paradigm === "master_theorem") {
      visualizerView.style.display = "none";
      detectiveView.style.display = "none";
      mtView.style.display = "block";
      return;
    }

    visualizerView.style.display = "grid";
    detectiveView.style.display = "none";
    mtView.style.display = "none";

    // Show pills corresponding to paradigm
    document.querySelectorAll(".algo-pill").forEach(pill => {
      const p = pill.getAttribute("data-paradigm");
      pill.style.display = p === paradigm ? "inline-flex" : "none";
    });

    // Select first algorithm in paradigm
    const firstPill = document.querySelector(`.algo-pill[data-paradigm="${paradigm}"]`);
    if (firstPill) {
      this.selectAlgorithm(firstPill.getAttribute("data-algo"));
    }
  }

  selectAlgorithm(algo) {
    this.currentAlgorithm = algo;
    document.querySelectorAll(".algo-pill").forEach(p => {
      p.classList.toggle("active", p.getAttribute("data-algo") === algo);
    });

    // Update Input Panel fields
    this.configureInputFields(algo);

    // Fetch and initialize trace
    this.loadAlgorithm(this.currentParadigm, algo);
  }

  configureInputFields(algo) {
    const inputFieldsContainer = document.getElementById("dynamic-inputs-area");
    if (!inputFieldsContainer) return;

    if (["merge_sort", "quick_sort", "max_subarray"].includes(algo)) {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>Array (comma-separated integers):</label>
          <input type="text" id="input-array" class="app-input" value="${algo === 'max_subarray' ? '-2, 1, -3, 4, -1, 2, 1, -5, 4' : '38, 27, 43, 3, 9, 82, 10'}" placeholder="e.g. 10, 4, 2, 8">
        </div>
      `;
    } else if (algo === "binary_search") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>Sorted Array:</label>
          <input type="text" id="input-array" class="app-input" value="2, 5, 8, 12, 16, 23, 38, 56, 72, 91">
        </div>
        <div class="input-group">
          <label>Target to Find:</label>
          <input type="number" id="input-target" class="app-input input-narrow" value="23">
        </div>
      `;
    } else if (algo === "knapsack01") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>Weights:</label>
          <input type="text" id="input-weights" class="app-input" value="2, 3, 4, 5">
        </div>
        <div class="input-group">
          <label>Values:</label>
          <input type="text" id="input-values" class="app-input" value="3, 4, 5, 8">
        </div>
        <div class="input-group">
          <label>Capacity (W):</label>
          <input type="number" id="input-capacity" class="app-input input-narrow" value="8" min="1" max="25">
        </div>
      `;
    } else if (algo === "fractional_knapsack") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>Items (Weight:Value pairs, comma separated):</label>
          <input type="text" id="input-items" class="app-input" value="10:60, 20:100, 30:120">
        </div>
        <div class="input-group">
          <label>Capacity (kg):</label>
          <input type="number" id="input-capacity" class="app-input input-narrow" value="50">
        </div>
      `;
    } else if (algo === "lcs") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>String 1:</label>
          <input type="text" id="input-s1" class="app-input" value="AGGTAB">
        </div>
        <div class="input-group">
          <label>String 2:</label>
          <input type="text" id="input-s2" class="app-input" value="GXTXAYB">
        </div>
      `;
    } else if (algo === "coin_change") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>Coins:</label>
          <input type="text" id="input-coins" class="app-input" value="1, 2, 5">
        </div>
        <div class="input-group">
          <label>Target Amount:</label>
          <input type="number" id="input-amount" class="app-input input-narrow" value="11" min="1" max="50">
        </div>
      `;
    } else if (algo === "dijkstra") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>Graph Nodes:</label>
          <input type="text" id="input-nodes" class="app-input" value="A, B, C, D, E">
        </div>
        <div class="input-group">
          <label>Source Node:</label>
          <input type="text" id="input-source" class="app-input input-narrow" value="A">
        </div>
      `;
    } else if (algo === "activity_selection") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>Activities (Start:Finish pairs):</label>
          <input type="text" id="input-activities" class="app-input" value="1:4, 3:5, 0:6, 5:7, 3:8, 5:9, 6:10, 8:11">
        </div>
      `;
    } else if (algo === "huffman") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>Character Frequencies (char:freq):</label>
          <input type="text" id="input-frequencies" class="app-input" value="A:5, B:9, C:12, D:13, E:16, F:45">
        </div>
      `;
    } else if (algo === "job_sequencing") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>Jobs (Deadline:Profit):</label>
          <input type="text" id="input-jobs" class="app-input" value="2:100, 1:19, 2:27, 1:25, 3:15">
        </div>
      `;
    } else if (algo === "mcm") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>Matrix Dimensions Sequence:</label>
          <input type="text" id="input-dims" class="app-input" value="10, 30, 5, 60">
        </div>
      `;
    } else if (algo === "fibonacci") {
      inputFieldsContainer.innerHTML = `
        <div class="input-group">
          <label>n (Fibonacci number):</label>
          <input type="number" id="input-n" class="app-input input-narrow" value="8" min="1" max="25">
        </div>
      `;
    }
  }

  async loadAlgorithm(paradigm, algo, customPayload = null) {
    this.pause();
    this.setLoading(true);

    try {
      const payload = customPayload || this.buildPayloadFromInputs(algo);
      const response = await fetch(`/api/trace/${paradigm}/${algo}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Failed to load trace");
      }

      this.currentData = await response.json();
      this.steps = this.currentData.steps || [];
      this.currentStepIndex = 0;

      // Update UI headers
      document.getElementById("algo-title").textContent = this.currentData.algorithm;
      document.getElementById("algo-paradigm-badge").textContent = this.currentData.paradigm;
      document.getElementById("algo-time-complexity").textContent = this.currentData.time_complexity;
      document.getElementById("algo-space-complexity").textContent = this.currentData.space_complexity;

      // Load pseudocode
      this.loadPseudocode(this.currentData.pseudocode || []);

      // Load Multi-Language Code Snippet
      const activeLangBtn = document.querySelector(".lang-btn.active");
      const activeLang = activeLangBtn ? activeLangBtn.getAttribute("data-lang") : "python";
      this.updateCodeSnippet(activeLang);

      // Render step 0
      this.goToStep(0);
    } catch (err) {
      console.error(err);
      alert(`Error loading algorithm: ${err.message}`);
    } finally {
      this.setLoading(false);
    }
  }

  buildPayloadFromInputs(algo) {
    const payload = {};
    if (["merge_sort", "quick_sort", "max_subarray"].includes(algo)) {
      const raw = document.getElementById("input-array")?.value || "38, 27, 43, 3, 9, 82, 10";
      payload.array = raw.split(",").map(x => parseInt(x.trim(), 10)).filter(x => !isNaN(x));
    } else if (algo === "binary_search") {
      const raw = document.getElementById("input-array")?.value || "2, 5, 8, 12, 16, 23, 38, 56";
      payload.array = raw.split(",").map(x => parseInt(x.trim(), 10)).filter(x => !isNaN(x));
      payload.target = parseInt(document.getElementById("input-target")?.value || "23", 10);
    } else if (algo === "knapsack01") {
      payload.weights = (document.getElementById("input-weights")?.value || "2, 3, 4, 5").split(",").map(x => parseInt(x.trim(), 10));
      payload.values = (document.getElementById("input-values")?.value || "3, 4, 5, 8").split(",").map(x => parseInt(x.trim(), 10));
      payload.capacity = parseInt(document.getElementById("input-capacity")?.value || "8", 10);
    } else if (algo === "fractional_knapsack") {
      const itemsRaw = document.getElementById("input-items")?.value || "10:60, 20:100, 30:120";
      payload.items = itemsRaw.split(",").map((pair, idx) => {
        const [w, v] = pair.split(":").map(x => parseFloat(x.trim()));
        return { name: `Item ${idx + 1}`, weight: w, value: v };
      });
      payload.capacity = parseFloat(document.getElementById("input-capacity")?.value || "50");
    } else if (algo === "lcs") {
      payload.s1 = document.getElementById("input-s1")?.value || "AGGTAB";
      payload.s2 = document.getElementById("input-s2")?.value || "GXTXAYB";
    } else if (algo === "coin_change") {
      payload.coins = (document.getElementById("input-coins")?.value || "1, 2, 5").split(",").map(x => parseInt(x.trim(), 10));
      payload.amount = parseInt(document.getElementById("input-amount")?.value || "11", 10);
    } else if (algo === "activity_selection") {
      const raw = document.getElementById("input-activities")?.value || "1:4, 3:5, 0:6, 5:7";
      payload.activities = raw.split(",").map((p, idx) => {
        const [s, f] = p.split(":").map(x => parseInt(x.trim(), 10));
        return { id: `A${idx + 1}`, start: s, finish: f };
      });
    } else if (algo === "huffman") {
      const raw = document.getElementById("input-frequencies")?.value || "A:5, B:9, C:12";
      payload.frequencies = {};
      raw.split(",").forEach(p => {
        const [c, f] = p.split(":").map(x => x.trim());
        if (c && f) payload.frequencies[c] = parseInt(f, 10);
      });
    } else if (algo === "job_sequencing") {
      const raw = document.getElementById("input-jobs")?.value || "2:100, 1:19, 2:27";
      payload.jobs = raw.split(",").map((p, idx) => {
        const [d, pr] = p.split(":").map(x => parseInt(x.trim(), 10));
        return { id: `J${idx + 1}`, deadline: d, profit: pr };
      });
    } else if (algo === "mcm") {
      payload.dimensions = (document.getElementById("input-dims")?.value || "10, 30, 5, 60").split(",").map(x => parseInt(x.trim(), 10));
    } else if (algo === "fibonacci") {
      payload.n = parseInt(document.getElementById("input-n")?.value || "8", 10);
    }
    return payload;
  }

  loadPseudocode(lines) {
    const container = document.getElementById("pseudocode-list");
    if (!container) return;
    container.innerHTML = "";
    lines.forEach((line, idx) => {
      const row = document.createElement("div");
      row.className = "pseudo-line";
      row.setAttribute("data-line", idx + 1);
      row.innerHTML = `<span class="line-num">${idx + 1}</span><span class="line-code">${this.escapeHTML(line)}</span>`;
      container.appendChild(row);
    });
  }

  updateCodeSnippet(lang) {
    const codeEl = document.getElementById("code-snippet-pre");
    if (!codeEl) return;
    const snippets = ALGORITHM_CODE_SNIPPETS[this.currentAlgorithm] || {};
    const code = snippets[lang] || "// Implementation code coming soon.";
    codeEl.textContent = code;
  }

  goToStep(index) {
    if (!this.steps || !this.steps.length) return;
    this.currentStepIndex = Math.max(0, Math.min(this.steps.length - 1, index));
    const step = this.steps[this.currentStepIndex];

    // Update scrubber
    const scrubber = document.getElementById("step-scrubber");
    if (scrubber) {
      scrubber.max = this.steps.length - 1;
      scrubber.value = this.currentStepIndex;
    }

    const stepLabel = document.getElementById("step-counter-label");
    if (stepLabel) {
      stepLabel.textContent = `Step ${this.currentStepIndex + 1} of ${this.steps.length}`;
    }

    // Step Header Callout
    const titleEl = document.getElementById("step-title-callout");
    if (titleEl) titleEl.textContent = step.title;

    const descEl = document.getElementById("step-desc-callout");
    if (descEl) descEl.textContent = step.explanation;

    // Highlight pseudocode line
    document.querySelectorAll(".pseudo-line").forEach(l => l.classList.remove("active-line"));
    if (step.pseudocode_line) {
      const lineEl = document.querySelector(`.pseudo-line[data-line="${step.pseudocode_line}"]`);
      if (lineEl) {
        lineEl.classList.add("active-line");
        lineEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }
    }

    // Render Canvas based on algorithm
    const algo = this.currentAlgorithm;
    if (["merge_sort", "quick_sort", "binary_search", "max_subarray"].includes(algo)) {
      this.renderer.renderArrayBars(step.state, this.currentData.algorithm);
      if (algo === "merge_sort") {
        this.renderer.renderRecursionTree(step.state);
      }
    } else if (["knapsack01", "lcs", "mcm"].includes(algo)) {
      this.renderer.renderDPTable(step.state, this.currentData.algorithm);
    } else if (["coin_change", "fibonacci"].includes(algo)) {
      this.renderer.render1DArray(step.state, this.currentData.algorithm);
    } else if (algo === "fractional_knapsack") {
      this.renderer.renderFractionalKnapsack(step.state);
    } else if (algo === "dijkstra") {
      this.renderer.renderGraph(step.state);
    } else if (algo === "activity_selection") {
      this.renderer.renderActivities(step.state);
    } else if (algo === "job_sequencing") {
      this.renderer.renderJobSequencing(step.state);
    } else if (algo === "huffman") {
      this.renderer.renderHuffman(step.state);
    }

    // Update Metrics
    this.updateMetrics(step.metrics);

    // Update AI Tutor Commentary
    this.updateAIExplanation(step);

    // Audio tick
    this.playTone(320 + (this.currentStepIndex % 10) * 40, "sine", 0.04);
  }

  updateMetrics(metrics) {
    const container = document.getElementById("metrics-cards-grid");
    if (!container || !metrics) return;
    container.innerHTML = "";
    Object.entries(metrics).forEach(([key, val]) => {
      const card = document.createElement("div");
      card.className = "metric-card";
      card.innerHTML = `
        <div class="metric-label">${key.replace(/_/g, " ").toUpperCase()}</div>
        <div class="metric-value">${val}</div>
      `;
      container.appendChild(card);
    });
  }

  async updateAIExplanation(step) {
    const aiBox = document.getElementById("ai-tutor-explanation");
    const aiSourceBadge = document.getElementById("ai-source-badge");
    if (!aiBox) return;

    aiBox.innerHTML = `<span class="loading-pulse">Analyzing step with AI Engine...</span>`;
    try {
      const res = await window.aiCopilot.explainStep(this.currentData.algorithm, this.currentData.paradigm, step);
      aiBox.textContent = res.explanation;
      if (aiSourceBadge) aiSourceBadge.textContent = res.source || "DAA AI";
    } catch (e) {
      aiBox.textContent = step.explanation;
    }
  }

  togglePlay() {
    if (this.isPlaying) this.pause();
    else this.play();
  }

  play() {
    if (this.currentStepIndex >= this.steps.length - 1) {
      this.currentStepIndex = 0;
    }
    this.isPlaying = true;
    const playBtn = document.getElementById("btn-play");
    if (playBtn) playBtn.innerHTML = "⏸ Pause";

    this.playTimer = setInterval(() => {
      if (this.currentStepIndex < this.steps.length - 1) {
        this.stepForward();
      } else {
        this.pause();
      }
    }, this.playbackSpeed);
  }

  pause() {
    this.isPlaying = false;
    clearInterval(this.playTimer);
    const playBtn = document.getElementById("btn-play");
    if (playBtn) playBtn.innerHTML = "▶ Play";
  }

  stepForward() {
    if (this.currentStepIndex < this.steps.length - 1) {
      this.goToStep(this.currentStepIndex + 1);
    }
  }

  stepBackward() {
    if (this.currentStepIndex > 0) {
      this.goToStep(this.currentStepIndex - 1);
    }
  }

  resetVisualization() {
    this.pause();
    this.goToStep(0);
  }

  runCustomInput() {
    this.loadAlgorithm(this.currentParadigm, this.currentAlgorithm);
  }

  async generateAITestcase() {
    try {
      const select = document.getElementById("testcase-type-select");
      const caseType = select ? select.value : "random";
      const tc = await window.aiCopilot.generateTestcase(this.currentAlgorithm, caseType);

      // Populate into inputs
      if (tc.array && document.getElementById("input-array")) {
        document.getElementById("input-array").value = tc.array.join(", ");
      }
      if (tc.target !== undefined && document.getElementById("input-target")) {
        document.getElementById("input-target").value = tc.target;
      }
      if (tc.weights && document.getElementById("input-weights")) {
        document.getElementById("input-weights").value = tc.weights.join(", ");
      }
      if (tc.values && document.getElementById("input-values")) {
        document.getElementById("input-values").value = tc.values.join(", ");
      }
      if (tc.capacity && document.getElementById("input-capacity")) {
        document.getElementById("input-capacity").value = tc.capacity;
      }

      this.loadAlgorithm(this.currentParadigm, this.currentAlgorithm);
    } catch (e) {
      alert("Failed to generate AI testcase.");
    }
  }

  async runProblemDetective() {
    const input = document.getElementById("detective-input-text");
    const resultBox = document.getElementById("detective-result-card");
    if (!input || !resultBox) return;

    const text = input.value.trim();
    if (!text) {
      alert("Please enter a problem description first.");
      return;
    }

    resultBox.style.display = "block";
    resultBox.innerHTML = `<div class="loading-spinner"></div> Analyzing algorithmic properties with NLP Engine...`;

    try {
      const res = await window.aiCopilot.detectParadigm(text);
      resultBox.innerHTML = `
        <div class="detective-header">
          <div class="detective-title">Recommended Paradigm: <span class="paradigm-highlight">${res.paradigm}</span></div>
          <div class="detective-confidence">Confidence: <strong>${res.confidence_percentage}%</strong></div>
        </div>
        <div class="detective-algo">Suggested Algorithm: <strong>${res.recommended_algorithm}</strong></div>
        <div class="detective-reasoning"><p>${res.reasoning}</p></div>
        <div class="detective-math">
          <strong>State / Recurrence:</strong> <code>${res.state_or_recurrence}</code>
        </div>
        <div class="detective-complexities">
          <span>Time: <code>${res.time_complexity}</code></span> | 
          <span>Space: <code>${res.space_complexity}</code></span>
        </div>
        ${res.can_visualize && res.visualizer_route ? `
          <button id="btn-launch-visualizer" class="btn btn-primary" style="margin-top: 1rem;">
            🚀 Open in Visualizer with this Problem
          </button>
        ` : ''}
      `;

      const launchBtn = document.getElementById("btn-launch-visualizer");
      if (launchBtn) {
        launchBtn.addEventListener("click", () => {
          let targetParadigm = "divide_and_conquer";
          if (res.paradigm.includes("Greedy")) targetParadigm = "greedy";
          else if (res.paradigm.includes("Dynamic")) targetParadigm = "dynamic_programming";

          this.switchParadigm(targetParadigm);
          this.selectAlgorithm(res.visualizer_route);
        });
      }
    } catch (err) {
      resultBox.innerHTML = `<div class="error-msg">Error analyzing problem: ${err.message}</div>`;
    }
  }

  async loadPresetProblems() {
    const listContainer = document.getElementById("preset-problems-list");
    if (!listContainer || listContainer.children.length > 0) return;

    const presets = await window.aiCopilot.getPresetProblems();
    presets.forEach(p => {
      const card = document.createElement("div");
      card.className = "preset-card";
      card.innerHTML = `
        <div class="preset-title">${p.title}</div>
        <div class="preset-meta"><span class="badge-tag">${p.paradigm}</span></div>
        <div class="preset-desc">${p.problem}</div>
      `;
      card.addEventListener("click", () => {
        const input = document.getElementById("detective-input-text");
        if (input) input.value = p.problem;
        this.runProblemDetective();
      });
      listContainer.appendChild(card);
    });
  }

  async runMasterTheorem() {
    const a = parseFloat(document.getElementById("mt-a")?.value || "2");
    const b = parseFloat(document.getElementById("mt-b")?.value || "2");
    const k = parseFloat(document.getElementById("mt-k")?.value || "1");
    const p = parseFloat(document.getElementById("mt-p")?.value || "0");
    const resultBox = document.getElementById("mt-result-card");

    try {
      const res = await window.aiCopilot.solveMasterTheorem(a, b, k, p);
      resultBox.style.display = "block";
      resultBox.innerHTML = `
        <div class="mt-rec">Recurrence: <code>${res.recurrence}</code></div>
        <div class="mt-case">Classified Case: <strong>${res.master_case}</strong></div>
        <div class="mt-bound">Asymptotic Bound: <span class="complexity-badge">${res.asymptotic_bound}</span></div>
        <div class="mt-derivation"><p>${res.derivation}</p></div>
      `;
    } catch (e) {
      resultBox.style.display = "block";
      resultBox.innerHTML = `<div class="error-msg">${e.message}</div>`;
    }
  }

  setLoading(isLoading) {
    const spinner = document.getElementById("main-spinner");
    if (spinner) spinner.style.display = isLoading ? "flex" : "none";
  }

  escapeHTML(str) {
    return str.replace(/[&<>'"]/g, tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag));
  }
}

// Start application when DOM is ready
window.addEventListener("DOMContentLoaded", () => {
  window.daaApp = new DAAApp();
});
