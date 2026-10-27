"""
Dynamic Programming Algorithm Tracers
Generates step-by-step visualizer traces for:
- 0/1 Knapsack
- Longest Common Subsequence (LCS)
- Coin Change (Min Coins)
- Matrix Chain Multiplication (MCM)
- Fibonacci (Tabulation & Overlapping Subproblems)
"""

from typing import List, Dict, Any


def get_zero_one_knapsack_pseudocode() -> List[str]:
    return [
        "function knapsack01(weights, values, W):",
        "    dp = 2D array of size (n + 1) x (W + 1) initialized to 0",
        "    for i = 1 to n:",
        "        for w = 1 to W:",
        "            if weights[i - 1] <= w: // Can include item",
        "                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])",
        "            else:                   // Cannot include item",
        "                dp[i][w] = dp[i - 1][w]",
        "    return dp[n][W]"
    ]


def trace_zero_one_knapsack(weights: List[int], values: List[int], capacity: int) -> Dict[str, Any]:
    n = len(weights)
    W = capacity
    # dp table: (n+1) rows x (W+1) columns
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    steps = []

    items = [{"id": i + 1, "weight": weights[i], "value": values[i]} for i in range(n)]

    def record_step(title: str, explanation: str, line: int, curr_cell=None,
                    ref_cells=None, formula="", is_backtrack=False, backtrack_path=None):
        table_snapshot = [row[:] for row in dp]
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "dp_table": table_snapshot,
                "rows": n + 1,
                "cols": W + 1,
                "current_cell": curr_cell,
                "reference_cells": ref_cells or [],
                "formula": formula,
                "items": items,
                "capacity": W,
                "is_backtrack": is_backtrack,
                "backtrack_path": backtrack_path or []
            },
            "metrics": {
                "subproblems_solved": sum(1 for r in range(n + 1) for c in range(W + 1) if dp[r][c] > 0 or r == 0),
                "current_max_value": dp[curr_cell[0]][curr_cell[1]] if curr_cell else 0
            }
        })

    record_step(
        title="Initialize 2D DP Table",
        explanation=f"Creating (n+1)x(W+1) = {n+1}x{W+1} grid. Row 0 represents 0 items, Column 0 represents 0 capacity.",
        line=2
    )

    for i in range(1, n + 1):
        wt = weights[i - 1]
        val = values[i - 1]

        for w in range(1, W + 1):
            if wt <= w:
                exclude_val = dp[i - 1][w]
                include_val = val + dp[i - 1][w - wt]
                dp[i][w] = max(exclude_val, include_val)
                decision = "Include" if include_val >= exclude_val else "Exclude"
                formula = f"dp[{i}][{w}] = max(dp[{i-1}][{w}]={exclude_val}, val[{i-1}]={val} + dp[{i-1}][{w-wt}]={dp[i-1][w-wt]}) = {dp[i][w]}"

                record_step(
                    title=f"Cell ({i}, {w}): Item {i} (wt={wt}, val={val}) fits!",
                    explanation=f"Decision: {decision}. Compare excluding (value {exclude_val}) vs including (value {include_val}). Max is {dp[i][w]}.",
                    line=6,
                    curr_cell=[i, w],
                    ref_cells=[[i - 1, w], [i - 1, w - wt]],
                    formula=formula
                )
            else:
                dp[i][w] = dp[i - 1][w]
                formula = f"dp[{i}][{w}] = dp[{i-1}][{w}] = {dp[i][w]} (wt {wt} > capacity {w})"
                record_step(
                    title=f"Cell ({i}, {w}): Item {i} (wt={wt}) too heavy for cap {w}",
                    explanation=f"Cannot include item {i} because its weight {wt} exceeds sub-capacity {w}. Inheriting value {dp[i][w]} from top cell.",
                    line=8,
                    curr_cell=[i, w],
                    ref_cells=[[i - 1, w]],
                    formula=formula
                )

    # Backtracking to find chosen items
    chosen_items = []
    backtrack_path = []
    curr_w = W
    for i in range(n, 0, -1):
        backtrack_path.append([i, curr_w])
        if dp[i][curr_w] != dp[i - 1][curr_w]:
            chosen_items.append(items[i - 1])
            curr_w -= weights[i - 1]

    backtrack_path.append([0, curr_w])
    chosen_items.reverse()

    record_step(
        title="Backtracking Optimal Solution",
        explanation=f"Traced optimal subset of items: {[it['id'] for it in chosen_items]} giving max total value {dp[n][W]}.",
        line=9,
        curr_cell=[n, W],
        is_backtrack=True,
        backtrack_path=backtrack_path
    )

    return {
        "algorithm": "0/1 Knapsack",
        "paradigm": "Dynamic Programming",
        "pseudocode": get_zero_one_knapsack_pseudocode(),
        "time_complexity": "O(n * W) pseudo-polynomial",
        "space_complexity": "O(n * W) table (can optimize to O(W) with 1D array)",
        "optimal_substructure": "dp[i][w] = max(dp[i-1][w], val[i-1] + dp[i-1][w-wt[i-1]])",
        "steps": steps,
        "max_value": dp[n][W],
        "chosen_items": chosen_items,
        "dp_table": dp
    }


def get_lcs_pseudocode() -> List[str]:
    return [
        "function LCS(s1, s2):",
        "    m = s1.length, n = s2.length",
        "    dp = 2D array (m + 1) x (n + 1) filled with 0",
        "    for i = 1 to m:",
        "        for j = 1 to n:",
        "            if s1[i - 1] == s2[j - 1]:",
        "                dp[i][j] = 1 + dp[i - 1][j - 1] // Diagonal match",
        "            else:",
        "                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) // Up or Left",
        "    return dp[m][n]"
    ]


def trace_lcs(s1: str, s2: str) -> Dict[str, Any]:
    m = len(s1)
    n = len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    steps = []

    def record_step(title: str, explanation: str, line: int, curr_cell=None,
                    ref_cells=None, formula="", is_match=False, is_backtrack=False, backtrack_path=None):
        table_snapshot = [row[:] for row in dp]
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "dp_table": table_snapshot,
                "s1": s1,
                "s2": s2,
                "rows": m + 1,
                "cols": n + 1,
                "current_cell": curr_cell,
                "reference_cells": ref_cells or [],
                "formula": formula,
                "is_match": is_match,
                "is_backtrack": is_backtrack,
                "backtrack_path": backtrack_path or []
            },
            "metrics": {
                "lcs_length_so_far": dp[curr_cell[0]][curr_cell[1]] if curr_cell else 0
            }
        })

    record_step(
        title="Initialize LCS Matrix",
        explanation=f"Creating ({m+1})x({n+1}) grid for s1='{s1}' (vertical) and s2='{s2}' (horizontal).",
        line=3
    )

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            c1 = s1[i - 1]
            c2 = s2[j - 1]

            if c1 == c2:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                formula = f"dp[{i}][{j}] = 1 + dp[{i-1}][{j-1}] = {dp[i][j]}"
                record_step(
                    title=f"Match found! '{c1}' == '{c2}'",
                    explanation=f"Characters match at s1[{i-1}] and s2[{j-1}]. Take diagonal value {dp[i-1][j-1]} + 1 = {dp[i][j]}.",
                    line=7,
                    curr_cell=[i, j],
                    ref_cells=[[i - 1, j - 1]],
                    formula=formula,
                    is_match=True
                )
            else:
                up_val = dp[i - 1][j]
                left_val = dp[i][j - 1]
                dp[i][j] = max(up_val, left_val)
                formula = f"dp[{i}][{j}] = max(dp[{i-1}][{j}]={up_val}, dp[{i}][{j-1}]={left_val}) = {dp[i][j]}"
                record_step(
                    title=f"Mismatch: '{c1}' != '{c2}'",
                    explanation=f"Take maximum of top cell ({up_val}) and left cell ({left_val}) => {dp[i][j]}.",
                    line=9,
                    curr_cell=[i, j],
                    ref_cells=[[i - 1, j], [i, j - 1]],
                    formula=formula,
                    is_match=False
                )

    # Backtracking to recover the LCS string
    lcs_chars = []
    backtrack_path = []
    i, j = m, n
    while i > 0 and j > 0:
        backtrack_path.append([i, j])
        if s1[i - 1] == s2[j - 1]:
            lcs_chars.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    backtrack_path.append([i, j])
    lcs_string = "".join(reversed(lcs_chars))

    record_step(
        title=f"LCS Reconstructed: '{lcs_string}'",
        explanation=f"Followed backtrack arrows from cell ({m}, {n}) to (0, 0). Length of LCS is {dp[m][n]}.",
        line=10,
        curr_cell=[m, n],
        is_backtrack=True,
        backtrack_path=backtrack_path
    )

    return {
        "algorithm": "Longest Common Subsequence (LCS)",
        "paradigm": "Dynamic Programming",
        "pseudocode": get_lcs_pseudocode(),
        "time_complexity": "O(m * n)",
        "space_complexity": "O(m * n)",
        "optimal_substructure": "If s1[i-1] == s2[j-1]: 1 + dp[i-1][j-1], else max(dp[i-1][j], dp[i][j-1])",
        "steps": steps,
        "lcs_length": dp[m][n],
        "lcs_string": lcs_string,
        "dp_table": dp
    }


def get_coin_change_pseudocode() -> List[str]:
    return [
        "function coinChange(coins, amount):",
        "    dp = array of size (amount + 1) filled with infinity",
        "    dp[0] = 0",
        "    for a = 1 to amount:",
        "        for coin in coins:",
        "            if coin <= a:",
        "                dp[a] = min(dp[a], 1 + dp[a - coin])",
        "    return dp[amount] if dp[amount] != infinity else -1"
    ]


def trace_coin_change(coins: List[int], amount: int) -> Dict[str, Any]:
    INF = 999999
    dp = [INF] * (amount + 1)
    dp[0] = 0
    parent_coin = [-1] * (amount + 1)
    steps = []

    def record_step(title: str, explanation: str, line: int, curr_amount=None,
                    ref_amount=None, formula="", active_coin=None, is_backtrack=False, backtrack_coins=None):
        clean_dp = [("∞" if v == INF else v) for v in dp]
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "dp_array": clean_dp,
                "amount": amount,
                "coins": coins,
                "current_amount": curr_amount,
                "referenced_amount": ref_amount,
                "active_coin": active_coin,
                "formula": formula,
                "is_backtrack": is_backtrack,
                "backtrack_coins": backtrack_coins or []
            },
            "metrics": {
                "target_amount": amount,
                "coins_used_so_far": clean_dp[curr_amount] if curr_amount is not None else 0
            }
        })

    record_step(
        title="Initialize 1D DP Array for Coin Change",
        explanation=f"Target amount is {amount} with coin denominations {coins}. Base case: dp[0] = 0 coins.",
        line=3,
        curr_amount=0
    )

    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                prev_val = dp[a - c]
                candidate = prev_val + 1 if prev_val != INF else INF
                old_val = dp[a]
                
                if candidate < old_val:
                    dp[a] = candidate
                    parent_coin[a] = c
                    formula = f"dp[{a}] = min({('∞' if old_val == INF else old_val)}, 1 + dp[{a - c}]={prev_val}) = {dp[a]}"
                    record_step(
                        title=f"Amount {a}: Try Coin {c} => New Min {dp[a]} Coins!",
                        explanation=f"Using coin {c} requires 1 + dp[{a - c}] = {dp[a]} total coins. Updated dp[{a}].",
                        line=7,
                        curr_amount=a,
                        ref_amount=a - c,
                        active_coin=c,
                        formula=formula
                    )
                else:
                    formula = f"dp[{a}] remained {('∞' if old_val == INF else old_val)} (using coin {c} gives {('∞' if candidate == INF else candidate)})"
                    record_step(
                        title=f"Amount {a}: Coin {c} gives no improvement",
                        explanation=f"Coin {c} doesn't beat current minimum of {('∞' if old_val == INF else old_val)}.",
                        line=7,
                        curr_amount=a,
                        ref_amount=a - c,
                        active_coin=c,
                        formula=formula
                    )

    # Backtracking coins used
    used_coins = []
    curr = amount
    if dp[amount] != INF:
        while curr > 0:
            c = parent_coin[curr]
            if c == -1:
                break
            used_coins.append(c)
            curr -= c

    clean_dp = [("∞" if v == INF else v) for v in dp]
    record_step(
        title=f"Coin Change Complete: Minimum {clean_dp[amount]} Coins",
        explanation=f"Optimal combination of coins to make amount {amount}: {used_coins} (sum = {sum(used_coins)}).",
        line=8,
        curr_amount=amount,
        is_backtrack=True,
        backtrack_coins=used_coins
    )

    return {
        "algorithm": "Coin Change (Minimum Coins)",
        "paradigm": "Dynamic Programming",
        "pseudocode": get_coin_change_pseudocode(),
        "time_complexity": "O(amount * number_of_coins)",
        "space_complexity": "O(amount) 1D table",
        "optimal_substructure": "dp[a] = min_{c in coins} (1 + dp[a - c])",
        "steps": steps,
        "min_coins": clean_dp[amount],
        "used_coins": used_coins,
        "dp_array": clean_dp
    }


def get_mcm_pseudocode() -> List[str]:
    return [
        "function matrixChainOrder(p):",
        "    n = p.length - 1 // Number of matrices",
        "    m = 2D array size (n + 1) x (n + 1) initialized to 0",
        "    for L = 2 to n:   // Chain length",
        "        for i = 1 to n - L + 1:",
        "            j = i + L - 1",
        "            m[i][j] = infinity",
        "            for k = i to j - 1:",
        "                cost = m[i][k] + m[k + 1][j] + p[i - 1]*p[k]*p[j]",
        "                if cost < m[i][j]: m[i][j] = cost; s[i][j] = k",
        "    return m[1][n]"
    ]


def trace_matrix_chain_multiplication(dims: List[int]) -> Dict[str, Any]:
    n = len(dims) - 1  # Number of matrices A1 to An
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]
    steps = []

    def record_step(title: str, explanation: str, line: int, curr_cell=None,
                    split_k=None, formula="", ref_cells=None):
        table_snapshot = [row[:] for row in m]
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "m_table": table_snapshot,
                "n_matrices": n,
                "dimensions": dims,
                "current_cell": curr_cell,
                "split_k": split_k,
                "formula": formula,
                "reference_cells": ref_cells or []
            },
            "metrics": {
                "current_min_cost": m[curr_cell[0]][curr_cell[1]] if curr_cell else 0
            }
        })

    record_step(
        title="Initialize MCM Upper Triangular Table",
        explanation=f"Given {n} matrices with dimension vector {dims}. Base case: m[i][i] = 0 (single matrix costs 0 operations).",
        line=3
    )

    for L in range(2, n + 1):
        for i in range(1, n - L + 2):
            j = i + L - 1
            m[i][j] = float("inf")

            record_step(
                title=f"Evaluating Chain A{i}..A{j} (Length {L})",
                explanation=f"Finding optimal split point k between {i} and {j - 1} for multiplying matrices A{i} to A{j}.",
                line=6,
                curr_cell=[i, j]
            )

            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
                    formula = f"m[{i}][{j}] = m[{i}][{k}] + m[{k+1}][{j}] + {dims[i-1]}*{dims[k]}*{dims[j]} = {cost} (split k={k})"
                    record_step(
                        title=f"Split at k={k}: New Minimum Cost {cost}",
                        explanation=f"Multiplying (A{i}..A{k}) and (A{k+1}..A{j}) requires {cost} scalar operations.",
                        line=10,
                        curr_cell=[i, j],
                        split_k=k,
                        formula=formula,
                        ref_cells=[[i, k], [k + 1, j]]
                    )

    def build_parentheses(i, j):
        if i == j:
            return f"A{i}"
        k = s[i][j]
        return f"({build_parentheses(i, k)} x {build_parentheses(k + 1, j)})"

    optimal_parens = build_parentheses(1, n)

    record_step(
        title="Matrix Chain Multiplication Complete",
        explanation=f"Minimum scalar multiplications: {m[1][n]}. Optimal order: {optimal_parens}.",
        line=11,
        curr_cell=[1, n],
        formula=f"Optimal Parenthesization: {optimal_parens}"
    )

    return {
        "algorithm": "Matrix Chain Multiplication (MCM)",
        "paradigm": "Dynamic Programming",
        "pseudocode": get_mcm_pseudocode(),
        "time_complexity": "O(n³)",
        "space_complexity": "O(n²)",
        "optimal_substructure": "m[i][j] = min_{k} (m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j])",
        "steps": steps,
        "min_operations": m[1][n],
        "optimal_parenthesization": optimal_parens,
        "m_table": m
    }


def get_fibonacci_pseudocode() -> List[str]:
    return [
        "function fibonacci(n):",
        "    dp = array of size (n + 1)",
        "    dp[0] = 0, dp[1] = 1",
        "    for i = 2 to n:",
        "        dp[i] = dp[i - 1] + dp[i - 2] // Overlapping subproblem solved once",
        "    return dp[n]"
    ]


def trace_fibonacci(n: int) -> Dict[str, Any]:
    dp = [0] * (n + 1)
    if n >= 1:
        dp[1] = 1
    steps = []

    def record_step(title: str, explanation: str, line: int, curr_i=None, ref_indices=None):
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "dp_array": list(dp),
                "n": n,
                "current_index": curr_i,
                "referenced_indices": ref_indices or []
            },
            "metrics": {
                "naive_recursive_calls": 2 ** curr_i if curr_i and curr_i <= 20 else "Exponential 2^n",
                "dp_operations": curr_i if curr_i else 1
            }
        })

    record_step(
        title="Initialize Fibonacci Base Cases",
        explanation=f"Base cases: dp[0] = 0, dp[1] = 1. Naive recursion computes overlapping calls exponentially O(2^n). DP tabulates in linear O(n).",
        line=3,
        curr_i=1
    )

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        record_step(
            title=f"Calculate dp[{i}] = dp[{i-1}] + dp[{i-2}] = {dp[i]}",
            explanation=f"Reusing already solved subproblems: dp[{i-1}] ({dp[i-1]}) + dp[{i-2}] ({dp[i-2]}) = {dp[i]}.",
            line=5,
            curr_i=i,
            ref_indices=[i - 1, i - 2]
        )

    record_step(
        title="Fibonacci Tabulation Complete",
        explanation=f"F({n}) = {dp[n]} computed in exactly {n} steps instead of {2**n if n <= 20 else 'billions'} recursive calls.",
        line=6,
        curr_i=n
    )

    return {
        "algorithm": "Fibonacci (DP Tabulation vs Overlapping Subproblems)",
        "paradigm": "Dynamic Programming",
        "pseudocode": get_fibonacci_pseudocode(),
        "time_complexity": "O(n) linear vs O(2^n) naive",
        "space_complexity": "O(n) table or O(1) two variables",
        "optimal_substructure": "F(n) = F(n-1) + F(n-2)",
        "steps": steps,
        "fib_value": dp[n],
        "dp_array": dp
    }
