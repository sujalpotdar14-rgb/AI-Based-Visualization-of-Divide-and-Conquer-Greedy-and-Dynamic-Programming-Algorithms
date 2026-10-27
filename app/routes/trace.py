"""
FastAPI Routes for Algorithm Execution and Traces
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from app.algorithms import (
    trace_merge_sort,
    trace_quick_sort,
    trace_binary_search,
    trace_max_subarray,
    trace_fractional_knapsack,
    trace_activity_selection,
    trace_dijkstra,
    trace_huffman_coding,
    trace_job_sequencing,
    trace_zero_one_knapsack,
    trace_lcs,
    trace_coin_change,
    trace_matrix_chain_multiplication,
    trace_fibonacci
)

router = APIRouter(prefix="/api/trace", tags=["Algorithm Trace"])


class TraceRequest(BaseModel):
    # For array algorithms (sorting, binary search, kadane)
    array: Optional[List[int]] = None
    target: Optional[int] = None

    # For Knapsack
    weights: Optional[List[int]] = None
    values: Optional[List[int]] = None
    capacity: Optional[float] = None
    items: Optional[List[Dict[str, Any]]] = None

    # For LCS
    s1: Optional[str] = None
    s2: Optional[str] = None

    # For Coin Change
    coins: Optional[List[int]] = None
    amount: Optional[int] = None

    # For Activities
    activities: Optional[List[Dict[str, Any]]] = None

    # For Dijkstra
    nodes: Optional[List[str]] = None
    edges: Optional[List[Dict[str, Any]]] = None
    source: Optional[str] = None

    # For Huffman
    frequencies: Optional[Dict[str, int]] = None

    # For Job Sequencing
    jobs: Optional[List[Dict[str, Any]]] = None

    # For MCM
    dimensions: Optional[List[int]] = None

    # For Fibonacci
    n: Optional[int] = None


@router.post("/{paradigm}/{algorithm}")
async def get_algorithm_trace(paradigm: str, algorithm: str, req: TraceRequest):
    p = paradigm.lower().replace("-", "_")
    algo = algorithm.lower().replace("-", "_")

    try:
        # Divide and Conquer
        if algo in ["merge_sort", "mergesort"]:
            arr = req.array or [38, 27, 43, 3, 9, 82, 10]
            if len(arr) > 40:
                raise HTTPException(status_code=400, detail="Array size limited to 40 for optimal visualization")
            return trace_merge_sort(arr)

        elif algo in ["quick_sort", "quicksort"]:
            arr = req.array or [10, 80, 30, 90, 40, 50, 70]
            if len(arr) > 40:
                raise HTTPException(status_code=400, detail="Array size limited to 40 for optimal visualization")
            return trace_quick_sort(arr)

        elif algo in ["binary_search", "binarysearch"]:
            arr = req.array or [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
            target = req.target if req.target is not None else 23
            return trace_binary_search(arr, target)

        elif algo in ["max_subarray", "kadane", "maximum_subarray"]:
            arr = req.array or [-2, 1, -3, 4, -1, 2, 1, -5, 4]
            return trace_max_subarray(arr)

        # Greedy
        elif algo in ["fractional_knapsack", "fractionalknapsack"]:
            items = req.items or [
                {"name": "Gold Ore", "weight": 10, "value": 60},
                {"name": "Silver Dust", "weight": 20, "value": 100},
                {"name": "Copper Mix", "weight": 30, "value": 120}
            ]
            cap = req.capacity if req.capacity is not None else 50.0
            return trace_fractional_knapsack(items, cap)

        elif algo in ["activity_selection", "activityselection", "interval_scheduling"]:
            acts = req.activities or [
                {"id": "A1", "start": 1, "finish": 4},
                {"id": "A2", "start": 3, "finish": 5},
                {"id": "A3", "start": 0, "finish": 6},
                {"id": "A4", "start": 5, "finish": 7},
                {"id": "A5", "start": 3, "finish": 8},
                {"id": "A6", "start": 5, "finish": 9},
                {"id": "A7", "start": 6, "finish": 10},
                {"id": "A8", "start": 8, "finish": 11}
            ]
            return trace_activity_selection(acts)

        elif algo in ["dijkstra", "shortest_path"]:
            nodes = req.nodes or ["A", "B", "C", "D", "E"]
            edges = req.edges or [
                {"from": "A", "to": "B", "weight": 4},
                {"from": "A", "to": "C", "weight": 2},
                {"from": "B", "to": "C", "weight": 1},
                {"from": "B", "to": "D", "weight": 5},
                {"from": "C", "to": "D", "weight": 8},
                {"from": "C", "to": "E", "weight": 10},
                {"from": "D", "to": "E", "weight": 2}
            ]
            src = req.source or "A"
            return trace_dijkstra({"nodes": nodes, "edges": edges, "undirected": True}, src)

        elif algo in ["huffman", "huffman_coding"]:
            freqs = req.frequencies or {"A": 5, "B": 9, "C": 12, "D": 13, "E": 16, "F": 45}
            return trace_huffman_coding(freqs)

        elif algo in ["job_sequencing", "jobsequencing"]:
            jobs = req.jobs or [
                {"id": "J1", "deadline": 2, "profit": 100},
                {"id": "J2", "deadline": 1, "profit": 19},
                {"id": "J3", "deadline": 2, "profit": 27},
                {"id": "J4", "deadline": 1, "profit": 25},
                {"id": "J5", "deadline": 3, "profit": 15}
            ]
            return trace_job_sequencing(jobs)

        # Dynamic Programming
        elif algo in ["knapsack01", "zero_one_knapsack", "01knapsack"]:
            wts = req.weights or [2, 3, 4, 5]
            vals = req.values or [3, 4, 5, 8]
            cap = int(req.capacity) if req.capacity is not None else 8
            if cap > 25:
                raise HTTPException(status_code=400, detail="Capacity limited to 25 for clear 2D grid display")
            return trace_zero_one_knapsack(wts, vals, cap)

        elif algo in ["lcs", "longest_common_subsequence"]:
            s1 = req.s1 or "AGGTAB"
            s2 = req.s2 or "GXTXAYB"
            if len(s1) > 20 or len(s2) > 20:
                raise HTTPException(status_code=400, detail="String lengths limited to 20 for matrix visualization")
            return trace_lcs(s1, s2)

        elif algo in ["coin_change", "coinchange"]:
            coins = req.coins or [1, 2, 5]
            amount = req.amount if req.amount is not None else 11
            if amount > 50:
                raise HTTPException(status_code=400, detail="Amount limited to 50 for clean 1D array display")
            return trace_coin_change(coins, amount)

        elif algo in ["mcm", "matrix_chain_multiplication"]:
            dims = req.dimensions or [10, 30, 5, 60]
            if len(dims) > 8:
                raise HTTPException(status_code=400, detail="Max 7 matrices for clear triangular table")
            return trace_matrix_chain_multiplication(dims)

        elif algo in ["fibonacci", "fib"]:
            n = req.n if req.n is not None else 8
            if n > 25:
                raise HTTPException(status_code=400, detail="n limited to 25")
            return trace_fibonacci(n)

        else:
            raise HTTPException(status_code=404, detail=f"Algorithm '{algorithm}' in paradigm '{paradigm}' not found.")

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Tracing error: {str(e)}")
