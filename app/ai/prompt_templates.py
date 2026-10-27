"""
AI Prompt Templates and Built-in Expert DAA Knowledge Base
"""

EXPERT_PARADIGM_KNOWLEDGE = {
    "divide_and_conquer": {
        "definition": "Breaks a problem down into two or more independent subproblems of the same type, solves each subproblem recursively, and then combines their solutions to solve the original problem.",
        "characteristics": [
            "Independent subproblems (no overlapping calculations)",
            "Recursive decomposition (typically halving or splitting by a factor)",
            "Conquer step: Base cases solved directly without recursion",
            "Combine step: Merging or aggregating subproblem answers"
        ],
        "key_algorithms": ["Merge Sort", "Quick Sort", "Binary Search", "Strassen's Matrix Multiplication", "Karatsuba Multiplication", "Closest Pair of Points"],
        "recurrence_form": "T(n) = a*T(n/b) + f(n) (Master Theorem applies)",
        "indicators": ["divide into halves", "sort subarrays", "partition around pivot", "bisect range", "independent sub-ranges"]
    },
    "greedy": {
        "definition": "Builds up a solution piece by piece, always choosing the next piece that offers the most immediate (local) benefit without looking ahead or reconsidering previous choices.",
        "characteristics": [
            "Greedy Choice Property: A globally optimal solution can be arrived at by making locally optimal (greedy) choices.",
            "Optimal Substructure: An optimal solution to the problem contains within it optimal solutions to subproblems.",
            "No Backtracking: Once a choice is made, it is never undone.",
            "Often requires sorting or a priority queue as a preprocessing step."
        ],
        "key_algorithms": ["Fractional Knapsack", "Dijkstra's Algorithm", "Prim's & Kruskal's MST", "Activity Selection", "Huffman Coding", "Job Sequencing"],
        "recurrence_form": "Direct iterative selection without table or recursion tree",
        "indicators": ["highest ratio", "earliest finish time", "minimum weight", "shortest edge", "locally optimal", "fractional items", "greedy choice"]
    },
    "dynamic_programming": {
        "definition": "Solves complex optimization problems by breaking them down into simpler, overlapping subproblems, storing the results in a lookup table (memoization or tabulation) to ensure each subproblem is computed only once.",
        "characteristics": [
            "Overlapping Subproblems: The problem revisits the exact same subproblems repeatedly.",
            "Optimal Substructure: The optimal solution to the problem is formed from optimal solutions to its subproblems.",
            "Memoization (Top-Down with caching) or Tabulation (Bottom-Up 1D/2D table).",
            "State Transition Equation (Bellman Equation) defining dp[state]."
        ],
        "key_algorithms": ["0/1 Knapsack", "Longest Common Subsequence (LCS)", "Coin Change", "Matrix Chain Multiplication", "Floyd-Warshall", "Bellman-Ford", "Edit Distance"],
        "recurrence_form": "dp[i][j] = combine(dp[i-1][j], dp[i][j-1], ...)",
        "indicators": ["0/1 items without splitting", "longest subsequence", "minimum coins", "optimal parenthesization", "overlapping states", "table filling", "maximize profit without fractions"]
    }
}

PARADIGM_CLASSIFIER_PROMPT = """
You are an expert Professor of Algorithms (Design and Analysis of Algorithms - DAA).
Analyze the following problem statement and classify which algorithmic paradigm is best suited:
1. Divide and Conquer
2. Greedy Algorithm
3. Dynamic Programming

Problem Statement:
"{problem_text}"

Return a JSON response with the following schema:
{{
  "paradigm": "Divide and Conquer | Greedy | Dynamic Programming",
  "confidence_percentage": 95,
  "recommended_algorithm": "Name of standard algorithm (e.g., Fractional Knapsack, 0/1 Knapsack, Merge Sort, etc.)",
  "time_complexity": "e.g., O(n log n)",
  "space_complexity": "e.g., O(n)",
  "reasoning": "Clear explanation of why this paradigm applies (discussing optimal substructure, overlapping subproblems, or greedy choice property)",
  "state_or_recurrence": "State transition equation or recurrence relation",
  "sample_input": {{ "key": "value" }},
  "can_visualize": true,
  "visualizer_route": "merge_sort | quick_sort | binary_search | fractional_knapsack | dijkstra | activity_selection | huffman | job_sequencing | knapsack01 | lcs | coin_change | mcm | fibonacci"
}}
"""

STEP_EXPLAINER_PROMPT = """
You are an AI Algorithm Tutor. Explain what is happening at this specific step in the execution of {algorithm_name} ({paradigm}):

Step Title: {step_title}
Current Action: {step_explanation}
Formula / Recurrence: {formula}
Active State Snapshot: {state_summary}

Provide a concise, intuitive 2-3 sentence explanation:
1. Why the algorithm made this specific decision at this step.
2. What algorithmic invariant is maintained.
3. How this step progresses towards the global optimal solution.
"""
