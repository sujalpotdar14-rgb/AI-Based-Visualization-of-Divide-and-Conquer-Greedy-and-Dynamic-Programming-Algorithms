/**
 * AI Copilot Module
 * Handles:
 * 1. Step Explanation (Gemini API + Built-in Rule Engine)
 * 2. Problem Paradigm Detective (NLP Problem Classification)
 * 3. Master Theorem Calculator
 * 4. AI Testcase Generator
 * 5. Gemini API Key Management
 */

class AICopilot {
  constructor() {
    this.apiKey = localStorage.getItem("gemini_api_key") || "";
  }

  getHeaders() {
    const headers = { "Content-Type": "application/json" };
    if (this.apiKey) {
      headers["x-gemini-key"] = this.apiKey;
    }
    return headers;
  }

  setApiKey(key) {
    this.apiKey = key.trim();
    if (this.apiKey) {
      localStorage.setItem("gemini_api_key", this.apiKey);
    } else {
      localStorage.removeItem("gemini_api_key");
    }
  }

  async explainStep(algorithm, paradigm, step) {
    try {
      const response = await fetch("/api/ai/explain-step", {
        method: "POST",
        headers: this.getHeaders(),
        body: JSON.stringify({ algorithm, paradigm, step })
      });
      if (!response.ok) throw new Error("Failed to get explanation");
      return await response.json();
    } catch (err) {
      console.warn("AI explain step fallback:", err);
      return {
        source: "Client Fallback",
        explanation: `${step.explanation} (This step maintains the algorithmic invariant and progresses towards optimal solution).`,
        status: "success"
      };
    }
  }

  async detectParadigm(problemText) {
    const response = await fetch("/api/ai/detect-paradigm", {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ problem_text: problemText })
    });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Failed to analyze problem");
    }
    return await response.json();
  }

  async solveMasterTheorem(a, b, k, p = 0) {
    const response = await fetch("/api/ai/master-theorem", {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ a, b, k, p })
    });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Calculation error");
    }
    return await response.json();
  }

  async generateTestcase(algorithm, caseType = "random") {
    const response = await fetch("/api/ai/generate-testcase", {
      method: "POST",
      headers: this.getHeaders(),
      body: JSON.stringify({ algorithm, case_type: caseType })
    });
    if (!response.ok) throw new Error("Failed to generate testcase");
    return await response.json();
  }

  async getPresetProblems() {
    const response = await fetch("/api/ai/preset-problems");
    if (!response.ok) return [];
    return await response.json();
  }
}

window.aiCopilot = new AICopilot();
