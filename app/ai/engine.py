"""
AI Engine for Algorithm Explanations, Paradigm Detection, and Complexity Analysis
Supports Google Gemini API with fallback to built-in Rule-Based DAA Expert Engine.
"""

import os
import math
import re
import json
from typing import Dict, Any, Optional

from .prompt_templates import EXPERT_PARADIGM_KNOWLEDGE, PARADIGM_CLASSIFIER_PROMPT, STEP_EXPLAINER_PROMPT

try:
    from google import genai
    HAS_GENAI_LIB = True
except ImportError:
    HAS_GENAI_LIB = False


class AIEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")

    def _get_client(self, custom_key: Optional[str] = None):
        key = custom_key or self.api_key or os.getenv("GEMINI_API_KEY", "")
        if key and HAS_GENAI_LIB:
            try:
                return genai.Client(api_key=key)
            except Exception:
                return None
        return None

    def explain_step(self, algorithm: str, paradigm: str, step_data: Dict[str, Any], custom_key: Optional[str] = None) -> Dict[str, Any]:
        """Explains a step using Gemini if available, or expert heuristic model."""
        client = self._get_client(custom_key)
        
        step_title = step_data.get("title", "")
        step_explanation = step_data.get("explanation", "")
        formula = step_data.get("state", {}).get("formula", "N/A")
        state_summary = str({k: v for k, v in step_data.get("state", {}).items() if k not in ["dp_table", "all_nodes"]})

        if client:
            try:
                prompt = STEP_EXPLAINER_PROMPT.format(
                    algorithm_name=algorithm,
                    paradigm=paradigm,
                    step_title=step_title,
                    step_explanation=step_explanation,
                    formula=formula,
                    state_summary=state_summary[:500]
                )
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                if response and response.text:
                    return {
                        "source": "gemini-2.5-flash",
                        "explanation": response.text.strip(),
                        "status": "success"
                    }
            except Exception as e:
                pass  # Fall back to built-in expert engine

        # Built-in DAA Expert Engine
        heuristic_explanation = self._rule_based_step_explanation(algorithm, paradigm, step_data)
        return {
            "source": "DAA Expert Rule Engine",
            "explanation": heuristic_explanation,
            "status": "success"
        }

    def _rule_based_step_explanation(self, algorithm: str, paradigm: str, step_data: Dict[str, Any]) -> str:
        title = step_data.get("title", "")
        explanation = step_data.get("explanation", "")
        state = step_data.get("state", {})

        if "Merge Sort" in algorithm:
            if "Divide" in title:
                return f"Divide Step: The algorithm breaks the problem down into two disjoint subproblems. Recurrence branches: T(n) splits into 2 subproblems of size n/2. No comparison work is done yet—only index bisection."
            elif "Compare" in title:
                return f"Conquer Step: Comparing two elements from the already sorted left and right sub-arrays. Because both subarrays are sorted, taking the smaller of the two preserves global sorted order (Two-Pointer Invariant)."
            elif "Place" in title or "Merged" in title:
                return f"Merge Invariant: The smaller element is placed into the auxiliary merged buffer. This maintains the sorted prefix invariant for the current range in O(n) total time."
        
        elif "Quick Sort" in algorithm:
            if "Pivot" in title:
                return f"Pivot Selection: Chosen pivot element will act as the partition boundary. All elements <= pivot are shifted to the left, and elements > pivot to the right in O(n) linear scan."
            elif "Swap" in title:
                return f"Lomuto Partitioning: Swapping ensures that elements smaller than the pivot remain grouped at indices [low...i], expanding the left partition boundary."
            elif "sorted index" in title:
                return f"Partition Invariant Achieved: The pivot is placed into its final, permanent position in the sorted array. The problem is now divided into two independent sub-arrays without needing a combine phase."

        elif "Binary Search" in algorithm:
            if "mid" in title:
                return f"Bisection Principle: Checking the middle element allows the algorithm to eliminate exactly half the remaining search space. Recurrence: T(n) = T(n/2) + O(1), leading to O(log n) efficiency."
            elif "Found" in title:
                return f"Termination Condition: Element matches target at middle index. Search terminates successfully in logarithmic time."
            else:
                return f"Pruning: Based on the array's sorted order, the target cannot exist in the rejected half, so that half is safely discarded."

        elif "0/1 Knapsack" in algorithm:
            if "fits" in title:
                return f"Optimal Substructure (Bellman Equation): For capacity {state.get('current_cell', [0,0])[1]}, we compare excluding item {state.get('current_cell', [0,0])[0]} vs including it. We take max(dp[i-1][w], val + dp[i-1][w-wt]). This resolves the 0/1 non-splittable decision."
            elif "too heavy" in title:
                return f"Feasibility Constraint: The item's weight exceeds the current column capacity. The optimal value remains identical to the best value achievable without this item (dp[i-1][w])."
            elif "Backtrack" in title:
                return f"Solution Reconstruction: Moving backwards through the DP grid by checking if dp[i][w] != dp[i-1][w] reveals which exact items were included in the optimal knapsack subset."

        elif "LCS" in algorithm:
            if "Match found" in title:
                return f"Optimal Substructure Match: Both characters match! Therefore, the longest common subsequence extends by 1, taking the optimal solution of both prefixes (1 + dp[i-1][j-1])."
            elif "Mismatch" in title:
                return f"Transition Decision: Since characters do not match, the LCS must either come from ignoring the character in s1 or ignoring the character in s2. We take max(dp[i-1][j], dp[i][j-1])."
            elif "Reconstructed" in title:
                return f"Backtracking: Following the match arrows diagonally up-left from (m, n) to (0, 0) reconstructs the exact characters belonging to the Longest Common Subsequence."

        elif "Fractional Knapsack" in algorithm:
            if "Ratio" in title:
                return f"Greedy Choice Invariant: Items are sorted by value density (value per unit weight). Picking items with the highest ratio guarantees optimal profit accumulation per kilogram."
            elif "100%" in title:
                return f"Full Item Inclusion: The item's entire weight fits within the remaining capacity, so we take 100% of its value."
            elif "fraction" in title:
                return f"Fractional Splitting: Unlike 0/1 Knapsack, the fractional knapsack allows slicing the item to consume exactly the remaining bag capacity."

        elif "Dijkstra" in algorithm:
            if "Extract Min" in title:
                return f"Greedy Choice Property: Node '{state.get('current_node')}' has the minimum tentative distance. Because edge weights are non-negative, no future path can possibly yield a shorter distance to this vertex."
            elif "Relax" in title:
                return f"Edge Relaxation Invariant: Path via '{state.get('current_node')}' yields a shorter route than previously known. Updating dist[v] maintains upper bounds on shortest paths."

        elif "Activity Selection" in algorithm:
            if "Select" in title:
                return f"Greedy Choice Property: Activity finishes earliest among remaining compatible activities. This leaves the largest possible remaining time interval to schedule further tasks."
            elif "Reject" in title:
                return f"Conflict Detected: Activity starts before the previously scheduled activity finishes. To maintain non-overlapping intervals, this activity must be skipped."

        return f"{explanation} This step maintains the algorithm's state invariant and progresses towards the globally optimal solution."

    def detect_paradigm(self, problem_text: str, custom_key: Optional[str] = None) -> Dict[str, Any]:
        """Analyzes an arbitrary algorithmic problem statement to determine the best paradigm."""
        client = self._get_client(custom_key)

        if client:
            try:
                prompt = PARADIGM_CLASSIFIER_PROMPT.format(problem_text=problem_text)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                if response and response.text:
                    cleaned = response.text.strip()
                    if cleaned.startswith("```json"):
                        cleaned = cleaned[7:-3].strip()
                    elif cleaned.startswith("```"):
                        cleaned = cleaned[3:-3].strip()
                    return json.loads(cleaned)
            except Exception:
                pass

        # Rule-based Natural Language Problem Classifier
        return self._rule_based_paradigm_detection(problem_text)

    def _rule_based_paradigm_detection(self, text: str) -> Dict[str, Any]:
        lower = text.lower()

        # Heuristic keywords mapping
        if any(w in lower for w in ["fractional", "knapsack with split", "ratio", "density"]):
            return {
                "paradigm": "Greedy",
                "confidence_percentage": 98,
                "recommended_algorithm": "Fractional Knapsack",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(1)",
                "reasoning": "Items can be split into fractions. Sorting by value-to-weight ratio exhibits the Greedy Choice Property: taking the highest density item first guarantees an optimal global solution.",
                "state_or_recurrence": "Greedy choice: Sort by value/weight descending; take full or fractional item.",
                "sample_input": {"capacity": 50, "items": [{"weight": 10, "value": 60}, {"weight": 20, "value": 100}, {"weight": 30, "value": 120}]},
                "can_visualize": True,
                "visualizer_route": "fractional_knapsack"
            }

        elif any(w in lower for w in ["knapsack", "0/1", "discrete", "bag", "weights and values", "capacity"]) and "fraction" not in lower:
            return {
                "paradigm": "Dynamic Programming",
                "confidence_percentage": 96,
                "recommended_algorithm": "0/1 Knapsack",
                "time_complexity": "O(n * W)",
                "space_complexity": "O(n * W)",
                "reasoning": "Items cannot be split (0 or 1 choice). Greedy fails here because taking the highest ratio item can leave unusable wasted capacity. Dynamic Programming evaluates overlapping subproblems with optimal substructure.",
                "state_or_recurrence": "dp[i][w] = max(dp[i-1][w], val[i-1] + dp[i-1][w - wt[i-1]])",
                "sample_input": {"capacity": 8, "weights": [2, 3, 4, 5], "values": [3, 4, 5, 8]},
                "can_visualize": True,
                "visualizer_route": "knapsack01"
            }

        elif any(w in lower for w in ["subsequence", "lcs", "common string", "dna alignment", "longest common"]):
            return {
                "paradigm": "Dynamic Programming",
                "confidence_percentage": 97,
                "recommended_algorithm": "Longest Common Subsequence (LCS)",
                "time_complexity": "O(m * n)",
                "space_complexity": "O(m * n)",
                "reasoning": "Characters in subsequences need not be contiguous. Overlapping subproblems arise when matching prefixes of both strings. Optimal substructure ensures optimal prefix alignment.",
                "state_or_recurrence": "dp[i][j] = 1 + dp[i-1][j-1] if match else max(dp[i-1][j], dp[i][j-1])",
                "sample_input": {"s1": "AGGTAB", "s2": "GXTXAYB"},
                "can_visualize": True,
                "visualizer_route": "lcs"
            }

        elif any(w in lower for w in ["coin", "coins", "change", "minimum coins", "denominations"]):
            return {
                "paradigm": "Dynamic Programming",
                "confidence_percentage": 95,
                "recommended_algorithm": "Coin Change (Minimum Coins)",
                "time_complexity": "O(amount * coins)",
                "space_complexity": "O(amount)",
                "reasoning": "For arbitrary coin denominations (e.g., coins [1, 3, 4] for amount 6), a greedy approach fails (picking 4 leaves 1+1 = 3 coins, whereas 3+3 = 2 coins is optimal). Dynamic Programming guarantees finding the true minimum.",
                "state_or_recurrence": "dp[a] = min_{c in coins} (1 + dp[a - c])",
                "sample_input": {"amount": 11, "coins": [1, 2, 5]},
                "can_visualize": True,
                "visualizer_route": "coin_change"
            }

        elif any(w in lower for w in ["activity", "meeting", "interval", "scheduling", "classroom", "finish time"]):
            return {
                "paradigm": "Greedy",
                "confidence_percentage": 95,
                "recommended_algorithm": "Activity Selection / Interval Scheduling",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(1)",
                "reasoning": "Selecting the compatible activity with the Earliest Finish Time (EFT) leaves the largest remaining continuous block of time for remaining activities. An exchange argument proves this greedy choice is globally optimal.",
                "state_or_recurrence": "Sort by finish time ascending; select next non-overlapping activity.",
                "sample_input": {"activities": [{"start": 1, "finish": 4}, {"start": 3, "finish": 5}, {"start": 0, "finish": 6}, {"start": 5, "finish": 7}, {"start": 8, "finish": 9}]},
                "can_visualize": True,
                "visualizer_route": "activity_selection"
            }

        elif any(w in lower for w in ["shortest path", "dijkstra", "graph distance", "route", "gps"]):
            return {
                "paradigm": "Greedy",
                "confidence_percentage": 96,
                "recommended_algorithm": "Dijkstra's Algorithm",
                "time_complexity": "O((V + E) log V)",
                "space_complexity": "O(V)",
                "reasoning": "With non-negative edge weights, the vertex with the minimum provisional distance can be greedily finalized because no future path can reduce its distance.",
                "state_or_recurrence": "dist[v] = min(dist[v], dist[u] + weight(u, v))",
                "sample_input": {"source": "A", "nodes": ["A", "B", "C", "D"], "edges": [{"from": "A", "to": "B", "weight": 4}, {"from": "A", "to": "C", "weight": 2}]},
                "can_visualize": True,
                "visualizer_route": "dijkstra"
            }

        elif any(w in lower for w in ["merge sort", "merge", "divide and conquer", "split in half", "divide array"]):
            return {
                "paradigm": "Divide and Conquer",
                "confidence_percentage": 98,
                "recommended_algorithm": "Merge Sort",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "reasoning": "The problem naturally splits into two completely independent subproblems of size n/2. Solutions are recursively conquered and combined using linear two-pointer merging.",
                "state_or_recurrence": "T(n) = 2T(n/2) + O(n) => Master Theorem Case 2",
                "sample_input": {"array": [38, 27, 43, 3, 9, 82, 10]},
                "can_visualize": True,
                "visualizer_route": "merge_sort"
            }

        elif any(w in lower for w in ["quick sort", "pivot", "partition"]):
            return {
                "paradigm": "Divide and Conquer",
                "confidence_percentage": 95,
                "recommended_algorithm": "Quick Sort",
                "time_complexity": "Average O(n log n), Worst O(n²)",
                "space_complexity": "O(log n)",
                "reasoning": "Partitions array in-place around a chosen pivot, then independently sorts the elements to the left and elements to the right. No separate combine phase is required.",
                "state_or_recurrence": "T(n) = T(k) + T(n - k - 1) + O(n)",
                "sample_input": {"array": [10, 80, 30, 90, 40, 50, 70]},
                "can_visualize": True,
                "visualizer_route": "quick_sort"
            }

        elif any(w in lower for w in ["binary search", "sorted array search", "bisect", "half the search"]):
            return {
                "paradigm": "Divide and Conquer",
                "confidence_percentage": 99,
                "recommended_algorithm": "Binary Search",
                "time_complexity": "O(log n)",
                "space_complexity": "O(1)",
                "reasoning": "Bisects the search space at the midpoint. Since the input array is monotonic (sorted), one entire half of the subproblem is pruned in constant O(1) time.",
                "state_or_recurrence": "T(n) = T(n/2) + O(1) => Master Theorem Case 2",
                "sample_input": {"array": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], "target": 23},
                "can_visualize": True,
                "visualizer_route": "binary_search"
            }

        elif any(w in lower for w in ["huffman", "compression", "frequency tree", "prefix code"]):
            return {
                "paradigm": "Greedy",
                "confidence_percentage": 98,
                "recommended_algorithm": "Huffman Coding",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "reasoning": "Greedily combines the two subtrees with the lowest character frequencies at each step, ensuring high-frequency symbols receive the shortest bit codes.",
                "state_or_recurrence": "Greedy priority queue min-extraction",
                "sample_input": {"frequencies": {"A": 5, "B": 9, "C": 12, "D": 13, "E": 16, "F": 45}},
                "can_visualize": True,
                "visualizer_route": "huffman"
            }

        elif any(w in lower for w in ["matrix chain", "parenthesization", "mcm", "matrix multiplication order"]):
            return {
                "paradigm": "Dynamic Programming",
                "confidence_percentage": 97,
                "recommended_algorithm": "Matrix Chain Multiplication (MCM)",
                "time_complexity": "O(n³)",
                "space_complexity": "O(n²)",
                "reasoning": "Matrix multiplication is associative. To find the optimal parenthesization of A_i...A_j, we split at every possible index k and memoize the subproblems in a triangular DP table.",
                "state_or_recurrence": "m[i][j] = min_{k} (m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j])",
                "sample_input": {"dimensions": [10, 30, 5, 60]},
                "can_visualize": True,
                "visualizer_route": "mcm"
            }

        # General classification fallback
        return {
            "paradigm": "Dynamic Programming",
            "confidence_percentage": 82,
            "recommended_algorithm": "Dynamic Programming / Memoization",
            "time_complexity": "O(n²)",
            "space_complexity": "O(n)",
            "reasoning": "The problem presents sequential decisions with overlapping states where past decisions influence future choices. Dynamic programming or state memoization provides optimal guarantees.",
            "state_or_recurrence": "dp[state] = optimal_transition(dp[next_state])",
            "sample_input": {"n": 10},
            "can_visualize": True,
            "visualizer_route": "fibonacci"
        }

    def solve_master_theorem(self, a: float, b: float, k: float, p: float = 0.0) -> Dict[str, Any]:
        """
        Solves Master Theorem for recurrence:
        T(n) = a * T(n / b) + Theta(n^k * (log n)^p)
        where a >= 1, b > 1, k >= 0
        """
        log_b_a = math.log(a, b)
        epsilon = 0.0001

        diff = k - log_b_a

        if abs(diff) < epsilon:
            # Case 2: k == log_b(a)
            if p > -1:
                result_complexity = f"Theta(n^{round(k, 2)} log^{p + 1} n)" if k != 1 else f"Theta(n log^{p + 1} n)"
            elif abs(p - (-1)) < epsilon:
                result_complexity = f"Theta(n^{round(k, 2)} log log n)"
            else:
                result_complexity = f"Theta(n^{round(k, 2)})"

            case = "Case 2 (Balanced Branching)"
            explanation = f"Since log_b(a) = log_{b}({a}) = {round(log_b_a, 3)} equals k = {k}, work is distributed evenly across all recursion tree levels. Multiply f(n) by log n."
        
        elif diff < 0:
            # Case 1: log_b(a) > k
            c_val = round(log_b_a, 3)
            result_complexity = f"Theta(n^{c_val})" if c_val != 1 else "Theta(n)"
            case = "Case 1 (Leaf-Heavy / Root-Subordinate)"
            explanation = f"Since log_b(a) = {round(log_b_a, 3)} > k = {k}, the bottom leaf nodes of the recursion tree dominate the total running time."
        
        else:
            # Case 3: log_b(a) < k
            result_complexity = f"Theta(n^{round(k, 2)} log^{p} n)" if p > 0 else f"Theta(n^{round(k, 2)})"
            case = "Case 3 (Root-Heavy)"
            explanation = f"Since k = {k} > log_b(a) = {round(log_b_a, 3)}, the top root level work dominates the recursive subproblems (assuming regularity condition a*f(n/b) <= c*f(n))."

        return {
            "recurrence": f"T(n) = {a}T(n/{b}) + O(n^{k}" + (f" log^{p} n)" if p > 0 else ")"),
            "a": a,
            "b": b,
            "k": k,
            "log_b_a": round(log_b_a, 3),
            "master_case": case,
            "asymptotic_bound": result_complexity,
            "derivation": explanation
        }

    def generate_testcase(self, algorithm: str, case_type: str = "random") -> Dict[str, Any]:
        """Generates tailored inputs: random, worst_case, best_case, edge_case."""
        if "Merge Sort" in algorithm:
            if case_type == "worst_case":
                return {"array": [8, 4, 2, 6, 1, 5, 3, 7], "type": "Interleaved worst-case comparisons"}
            elif case_type == "best_case":
                return {"array": [1, 2, 3, 4, 5, 6, 7, 8], "type": "Already sorted"}
            else:
                return {"array": [38, 27, 43, 3, 9, 82, 10], "type": "Random array"}

        elif "Quick Sort" in algorithm:
            if case_type == "worst_case":
                return {"array": [10, 20, 30, 40, 50, 60, 70], "type": "Already sorted (O(n²) for end-pivot)"}
            elif case_type == "best_case":
                return {"array": [40, 20, 60, 10, 30, 50, 70], "type": "Balanced pivot tree"}
            else:
                return {"array": [35, 10, 85, 45, 90, 25, 70], "type": "Random array"}

        elif "Binary Search" in algorithm:
            if case_type == "worst_case":
                return {"array": [1, 3, 5, 7, 9, 11, 13, 15], "target": 99, "type": "Target not present (max steps)"}
            elif case_type == "best_case":
                return {"array": [1, 3, 5, 7, 9, 11, 13, 15], "target": 7, "type": "Found immediately at mid (1 step)"}
            else:
                return {"array": [2, 5, 8, 12, 16, 23, 38, 56], "target": 23, "type": "Standard target"}

        elif "0/1 Knapsack" in algorithm:
            if case_type == "tricky_greedy_fails":
                # Classical example where greedy ratio fails
                return {
                    "capacity": 50,
                    "weights": [10, 20, 30],
                    "values": [60, 100, 120],
                    "type": "Ratio order: (6, 5, 4). Greedy picks item 1+2 (wt 30, val 160), but DP picks item 2+3 (wt 50, val 220)!"
                }
            else:
                return {"capacity": 7, "weights": [1, 3, 4, 5], "values": [1, 4, 5, 7], "type": "Standard knapsack"}

        elif "LCS" in algorithm:
            return {"s1": "AGGTAB", "s2": "GXTXAYB", "type": "Classic LCS"}

        elif "Coin Change" in algorithm:
            if case_type == "greedy_fails":
                return {"amount": 6, "coins": [1, 3, 4], "type": "Greedy picks 4+1+1 (3 coins), DP picks 3+3 (2 coins)!"}
            else:
                return {"amount": 11, "coins": [1, 2, 5], "type": "Standard US/Euro style denominations"}

        elif "Fractional Knapsack" in algorithm:
            return {
                "capacity": 50,
                "items": [
                    {"name": "Gold", "weight": 10, "value": 60},
                    {"name": "Silver", "weight": 20, "value": 100},
                    {"name": "Bronze", "weight": 30, "value": 120}
                ],
                "type": "Classic ratio items"
            }

        return {"input": "default"}


ai_engine = AIEngine()
