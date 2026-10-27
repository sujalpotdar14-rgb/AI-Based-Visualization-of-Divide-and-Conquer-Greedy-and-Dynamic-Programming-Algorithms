"""
Divide and Conquer Algorithm Tracers
Generates step-by-step visualizer traces for:
- Merge Sort
- Quick Sort
- Binary Search
- Maximum Subarray Sum (Divide & Conquer / Kadane)
"""

from typing import List, Dict, Any


def get_merge_sort_pseudocode() -> List[str]:
    return [
        "function mergeSort(arr, left, right):",
        "    if left >= right: return",
        "    mid = floor((left + right) / 2)",
        "    mergeSort(arr, left, mid)        // Divide left",
        "    mergeSort(arr, mid + 1, right)    // Divide right",
        "    merge(arr, left, mid, right)      // Conquer & Merge"
    ]


def trace_merge_sort(raw_arr: List[int]) -> Dict[str, Any]:
    arr = list(raw_arr)
    n = len(arr)
    steps = []
    comparisons = 0
    merges = 0

    tree_nodes = []
    node_counter = 0

    def record_step(title: str, explanation: str, line: int, active_range=None,
                    comparing=None, merged_indices=None, tree_state=None):
        nonlocal comparisons, merges
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "array": list(arr),
                "active_range": active_range or [0, n - 1],
                "comparing": comparing or [],
                "merged": merged_indices or [],
                "tree_node_id": tree_state.get("node_id") if tree_state else None,
                "tree_nodes": list(tree_nodes)
            },
            "metrics": {
                "comparisons": comparisons,
                "merges": merges,
                "array_size": n,
                "recurrence": "T(n) = 2T(n/2) + O(n)"
            }
        })

    def divide(left: int, right: int, depth: int, parent_id: str = None) -> str:
        nonlocal node_counter, comparisons, merges
        node_id = f"node_{node_counter}"
        node_counter += 1

        sub_arr = arr[left:right + 1]
        tree_node = {
            "id": node_id,
            "label": f"[{','.join(map(str, sub_arr))}]",
            "range": [left, right],
            "depth": depth,
            "parent": parent_id,
            "status": "dividing"
        }
        tree_nodes.append(tree_node)

        record_step(
            title=f"Divide Range [{left}...{right}]",
            explanation=f"Subproblem at indices {left} to {right}: array segment is {sub_arr}.",
            line=2 if left >= right else 3,
            active_range=[left, right],
            tree_state={"node_id": node_id}
        )

        if left >= right:
            tree_node["status"] = "base_case"
            record_step(
                title=f"Base Case reached at index {left}",
                explanation=f"Single element [{arr[left]}] is trivially sorted by definition.",
                line=2,
                active_range=[left, right],
                merged_indices=[left],
                tree_state={"node_id": node_id}
            )
            return node_id

        mid = (left + right) // 2

        record_step(
            title=f"Split at mid={mid}",
            explanation=f"Dividing into Left [{left}...{mid}] and Right [{mid+1}...{right}].",
            line=3,
            active_range=[left, right],
            tree_state={"node_id": node_id}
        )

        # Left recursion
        divide(left, mid, depth + 1, node_id)
        # Right recursion
        divide(mid + 1, right, depth + 1, node_id)

        # Merge step
        tree_node["status"] = "merging"
        record_step(
            title=f"Conquer & Merge [{left}...{mid}] and [{mid+1}...{right}]",
            explanation=f"Merging sorted halves: {arr[left:mid+1]} and {arr[mid+1:right+1]}.",
            line=6,
            active_range=[left, right],
            tree_state={"node_id": node_id}
        )

        # Actual Merge logic
        merges += 1
        left_copy = arr[left:mid + 1]
        right_copy = arr[mid + 1:right + 1]
        i = j = 0
        k = left

        while i < len(left_copy) and j < len(right_copy):
            comparisons += 1
            idx_left = left + i
            idx_right = mid + 1 + j

            record_step(
                title=f"Compare {left_copy[i]} vs {right_copy[j]}",
                explanation=f"Comparing element {left_copy[i]} from left sub-array and {right_copy[j]} from right sub-array.",
                line=6,
                active_range=[left, right],
                comparing=[idx_left, idx_right],
                tree_state={"node_id": node_id}
            )

            if left_copy[i] <= right_copy[j]:
                arr[k] = left_copy[i]
                record_step(
                    title=f"Place {left_copy[i]} at position {k}",
                    explanation=f"{left_copy[i]} <= {right_copy[j]}, so {left_copy[i]} is copied to merged position {k}.",
                    line=6,
                    active_range=[left, right],
                    merged_indices=list(range(left, k + 1)),
                    tree_state={"node_id": node_id}
                )
                i += 1
            else:
                arr[k] = right_copy[j]
                record_step(
                    title=f"Place {right_copy[j]} at position {k}",
                    explanation=f"{right_copy[j]} < {left_copy[i]}, so {right_copy[j]} is placed at merged position {k}.",
                    line=6,
                    active_range=[left, right],
                    merged_indices=list(range(left, k + 1)),
                    tree_state={"node_id": node_id}
                )
                j += 1
            k += 1

        while i < len(left_copy):
            arr[k] = left_copy[i]
            record_step(
                title=f"Flush remaining left element {left_copy[i]}",
                explanation=f"Copied remaining element {left_copy[i]} to index {k}.",
                line=6,
                active_range=[left, right],
                merged_indices=list(range(left, k + 1)),
                tree_state={"node_id": node_id}
            )
            i += 1
            k += 1

        while j < len(right_copy):
            arr[k] = right_copy[j]
            record_step(
                title=f"Flush remaining right element {right_copy[j]}",
                explanation=f"Copied remaining element {right_copy[j]} to index {k}.",
                line=6,
                active_range=[left, right],
                merged_indices=list(range(left, k + 1)),
                tree_state={"node_id": node_id}
            )
            j += 1
            k += 1

        tree_node["label"] = f"[{','.join(map(str, arr[left:right+1]))}]"
        tree_node["status"] = "sorted"
        record_step(
            title=f"Sub-array [{left}...{right}] Merged Successfully",
            explanation=f"Resulting sorted segment is {arr[left:right+1]}.",
            line=6,
            active_range=[left, right],
            merged_indices=list(range(left, right + 1)),
            tree_state={"node_id": node_id}
        )
        return node_id

    record_step(
        title="Initial Array",
        explanation="Starting Merge Sort on the input array.",
        line=1,
        active_range=[0, n - 1]
    )

    divide(0, n - 1, 0)

    record_step(
        title="Merge Sort Complete",
        explanation=f"Entire array has been sorted in O(n log n) time with {comparisons} comparisons and {merges} merge operations.",
        line=1,
        active_range=[0, n - 1],
        merged_indices=list(range(n))
    )

    return {
        "algorithm": "Merge Sort",
        "paradigm": "Divide and Conquer",
        "pseudocode": get_merge_sort_pseudocode(),
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "recurrence": "T(n) = 2T(n/2) + O(n)",
        "master_theorem_case": "Case 2 (log_b(a) = log_2(2) = 1, f(n) = O(n) => T(n) = Theta(n log n))",
        "steps": steps,
        "final_array": arr
    }


def get_quick_sort_pseudocode() -> List[str]:
    return [
        "function quickSort(arr, low, high):",
        "    if low < high:",
        "        pIndex = partition(arr, low, high)",
        "        quickSort(arr, low, pIndex - 1)  // Divide Left",
        "        quickSort(arr, pIndex + 1, high) // Divide Right",
        "function partition(arr, low, high):",
        "    pivot = arr[high], i = low - 1",
        "    for j = low to high - 1:",
        "        if arr[j] <= pivot: i++; swap(arr[i], arr[j])",
        "    swap(arr[i + 1], arr[high]); return i + 1"
    ]


def trace_quick_sort(raw_arr: List[int]) -> Dict[str, Any]:
    arr = list(raw_arr)
    n = len(arr)
    steps = []
    comparisons = 0
    swaps = 0
    sorted_indices = set()

    def record_step(title: str, explanation: str, line: int, low=0, high=n - 1,
                    pivot_idx=None, pointer_i=None, pointer_j=None, comparing=None, swapped=None):
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "array": list(arr),
                "low": low,
                "high": high,
                "pivot_index": pivot_idx,
                "pointer_i": pointer_i,
                "pointer_j": pointer_j,
                "comparing": comparing or [],
                "swapped": swapped or [],
                "sorted_indices": list(sorted_indices)
            },
            "metrics": {
                "comparisons": comparisons,
                "swaps": swaps,
                "sorted_count": len(sorted_indices),
                "recurrence": "T(n) = T(k) + T(n - k - 1) + O(n)"
            }
        })

    def partition(low: int, high: int) -> int:
        nonlocal comparisons, swaps
        pivot = arr[high]
        record_step(
            title=f"Choose Pivot: arr[{high}] = {pivot}",
            explanation=f"Selected {pivot} as pivot element for partition range [{low}...{high}].",
            line=7,
            low=low, high=high, pivot_idx=high, pointer_i=low - 1
        )

        i = low - 1
        for j in range(low, high):
            comparisons += 1
            record_step(
                title=f"Compare arr[{j}]={arr[j]} with Pivot={pivot}",
                explanation=f"Examining if arr[{j}] ({arr[j]}) is <= pivot ({pivot}).",
                line=9,
                low=low, high=high, pivot_idx=high, pointer_i=i, pointer_j=j,
                comparing=[j, high]
            )

            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    swaps += 1
                    record_step(
                        title=f"Swap arr[{i}] and arr[{j}]",
                        explanation=f"Since {arr[j]} <= {pivot}, increment pointer i to {i} and swap arr[{i}] with arr[{j}].",
                        line=9,
                        low=low, high=high, pivot_idx=high, pointer_i=i, pointer_j=j,
                        swapped=[i, j]
                    )
                else:
                    record_step(
                        title=f"Increment pointer i to {i}",
                        explanation=f"{arr[j]} <= {pivot}, elements already at index {i}.",
                        line=9,
                        low=low, high=high, pivot_idx=high, pointer_i=i, pointer_j=j
                    )

        # Put pivot in its final sorted position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1
        p_index = i + 1
        sorted_indices.add(p_index)

        record_step(
            title=f"Place Pivot at sorted index {p_index}",
            explanation=f"Swapped pivot {pivot} to index {p_index}. All elements to the left are <= {pivot}, and all to the right are > {pivot}.",
            line=10,
            low=low, high=high, pivot_idx=p_index, pointer_i=i + 1,
            swapped=[i + 1, high]
        )
        return p_index

    def quick_sort(low: int, high: int):
        if low < high:
            record_step(
                title=f"QuickSort Range [{low}...{high}]",
                explanation=f"Beginning partition for subproblem [{low}...{high}].",
                line=2,
                low=low, high=high
            )
            p = partition(low, high)
            quick_sort(low, p - 1)
            quick_sort(p + 1, high)
        elif low == high:
            sorted_indices.add(low)
            record_step(
                title=f"Single element at index {low}",
                explanation=f"Index {low} has only 1 element, already sorted.",
                line=2,
                low=low, high=high
            )

    record_step("Initial Array", "Starting Quick Sort algorithm.", 1)
    quick_sort(0, n - 1)
    sorted_indices.update(range(n))
    record_step(
        "Quick Sort Complete",
        f"Array fully sorted with {comparisons} comparisons and {swaps} swaps.",
        1,
        sorted_indices=list(range(n))
    )

    return {
        "algorithm": "Quick Sort",
        "paradigm": "Divide and Conquer",
        "pseudocode": get_quick_sort_pseudocode(),
        "time_complexity": "Average: O(n log n), Worst: O(n²)",
        "space_complexity": "O(log n) call stack",
        "recurrence": "T(n) = 2T(n/2) + O(n) (Best/Avg), T(n) = T(n-1) + O(n) (Worst)",
        "master_theorem_case": "Average: Case 2 => Theta(n log n)",
        "steps": steps,
        "final_array": arr
    }


def get_binary_search_pseudocode() -> List[str]:
    return [
        "function binarySearch(arr, target):",
        "    low = 0, high = arr.length - 1",
        "    while low <= high:",
        "        mid = floor((low + high) / 2)",
        "        if arr[mid] == target: return mid",
        "        else if arr[mid] < target: low = mid + 1",
        "        else: high = mid - 1",
        "    return -1 // Not found"
    ]


def trace_binary_search(raw_arr: List[int], target: int) -> Dict[str, Any]:
    # Ensure sorted
    arr = sorted(list(raw_arr))
    n = len(arr)
    steps = []
    comparisons = 0
    low = 0
    high = n - 1
    found_idx = -1

    def record_step(title: str, explanation: str, line: int, l: int, r: int, mid=None, match=False):
        nonlocal comparisons
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "array": list(arr),
                "target": target,
                "low": l,
                "high": r,
                "mid": mid,
                "eliminated_left": list(range(0, l)),
                "eliminated_right": list(range(r + 1, n)) if r + 1 <= n - 1 else [],
                "is_found": match
            },
            "metrics": {
                "comparisons": comparisons,
                "search_space_size": max(0, r - l + 1),
                "recurrence": "T(n) = T(n/2) + O(1)"
            }
        })

    record_step(
        title=f"Initialize Search Space for target={target}",
        explanation=f"Searching sorted array of size {n} between indices {low} and {high}.",
        line=2,
        l=low, r=high
    )

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1

        record_step(
            title=f"Calculate mid = ({low} + {high}) // 2 = {mid}",
            explanation=f"Inspecting middle element arr[{mid}] = {arr[mid]} against target {target}.",
            line=4,
            l=low, r=high, mid=mid
        )

        if arr[mid] == target:
            found_idx = mid
            record_step(
                title=f"Target {target} Found at index {mid}!",
                explanation=f"arr[{mid}] == {target}. Target successfully found in {comparisons} checks.",
                line=5,
                l=low, r=high, mid=mid, match=True
            )
            break
        elif arr[mid] < target:
            record_step(
                title=f"arr[{mid}]={arr[mid]} < target={target}",
                explanation=f"Target is larger than middle element. Eliminate left half [0...{mid}]. Move low to {mid + 1}.",
                line=6,
                l=low, r=high, mid=mid
            )
            low = mid + 1
        else:
            record_step(
                title=f"arr[{mid}]={arr[mid]} > target={target}",
                explanation=f"Target is smaller than middle element. Eliminate right half [{mid}...{high}]. Move high to {mid - 1}.",
                line=7,
                l=low, r=high, mid=mid
            )
            high = mid - 1

    if found_idx == -1:
        record_step(
            title="Target Not Found",
            explanation=f"Search space exhausted (low > high). Target {target} is not present in the array.",
            line=8,
            l=low, r=high
        )

    return {
        "algorithm": "Binary Search",
        "paradigm": "Divide and Conquer",
        "pseudocode": get_binary_search_pseudocode(),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "recurrence": "T(n) = T(n/2) + O(1)",
        "master_theorem_case": "Case 2 (a=1, b=2, k=0 => T(n) = Theta(log n))",
        "steps": steps,
        "target": target,
        "result_index": found_idx,
        "final_array": arr
    }


def get_max_subarray_pseudocode() -> List[str]:
    return [
        "function maxSubarray(arr):",
        "    max_so_far = arr[0], current_max = arr[0]",
        "    for i = 1 to arr.length - 1:",
        "        current_max = max(arr[i], current_max + arr[i])",
        "        max_so_far = max(max_so_far, current_max)",
        "    return max_so_far"
    ]


def trace_max_subarray(raw_arr: List[int]) -> Dict[str, Any]:
    arr = list(raw_arr)
    n = len(arr)
    steps = []

    current_max = arr[0]
    max_so_far = arr[0]
    best_start = 0
    best_end = 0
    curr_start = 0

    def record_step(title: str, explanation: str, line: int, curr_idx: int, window: list, best_window: list):
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "array": list(arr),
                "current_index": curr_idx,
                "current_max": current_max,
                "max_so_far": max_so_far,
                "current_window": window,
                "best_window": best_window
            },
            "metrics": {
                "max_sum": max_so_far,
                "current_sum": current_max,
                "iterations": curr_idx + 1
            }
        })

    record_step(
        title="Initialize Kadane's Window",
        explanation=f"Starting at index 0 with value {arr[0]}. max_so_far = {max_so_far}.",
        line=2,
        curr_idx=0,
        window=[0, 0],
        best_window=[0, 0]
    )

    for i in range(1, n):
        val = arr[i]
        if val > current_max + val:
            current_max = val
            curr_start = i
            record_step(
                title=f"Restart Subarray at index {i}",
                explanation=f"Element {val} alone is greater than extending previous sum ({current_max - val} + {val}). Starting new window at {i}.",
                line=4,
                curr_idx=i,
                window=[curr_start, i],
                best_window=[best_start, best_end]
            )
        else:
            current_max += val
            record_step(
                title=f"Extend Subarray to index {i}",
                explanation=f"Extending running window with {val} gives sum {current_max}.",
                line=4,
                curr_idx=i,
                window=[curr_start, i],
                best_window=[best_start, best_end]
            )

        if current_max > max_so_far:
            max_so_far = current_max
            best_start = curr_start
            best_end = i
            record_step(
                title=f"New Global Maximum: {max_so_far}!",
                explanation=f"Updated max_so_far to {max_so_far} spanning indices [{best_start}...{best_end}].",
                line=5,
                curr_idx=i,
                window=[curr_start, i],
                best_window=[best_start, best_end]
            )

    return {
        "algorithm": "Maximum Subarray Sum (Kadane's / D&C)",
        "paradigm": "Divide and Conquer",
        "pseudocode": get_max_subarray_pseudocode(),
        "time_complexity": "O(n) Kadane / O(n log n) Divide & Conquer",
        "space_complexity": "O(1)",
        "recurrence": "D&C: T(n) = 2T(n/2) + O(n) => O(n log n)",
        "steps": steps,
        "max_sum": max_so_far,
        "best_subarray": arr[best_start:best_end + 1],
        "best_indices": [best_start, best_end]
    }
