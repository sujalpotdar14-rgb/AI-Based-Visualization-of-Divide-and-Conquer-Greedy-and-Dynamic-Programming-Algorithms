"""
Greedy Algorithm Tracers
Generates step-by-step visualizer traces for:
- Fractional Knapsack
- Dijkstra's Shortest Path
- Activity Selection
- Huffman Coding
- Job Sequencing with Deadlines
"""

from typing import List, Dict, Any
import heapq


def get_fractional_knapsack_pseudocode() -> List[str]:
    return [
        "function fractionalKnapsack(items, capacity):",
        "    for each item in items: item.ratio = item.value / item.weight",
        "    sort items by ratio in descending order",
        "    total_value = 0, remaining_cap = capacity",
        "    for item in items:",
        "        if item.weight <= remaining_cap:  // Take full item",
        "            total_value += item.value; remaining_cap -= item.weight",
        "        else:                            // Take fractional part",
        "            total_value += item.value * (remaining_cap / item.weight)",
        "            break",
        "    return total_value"
    ]


def trace_fractional_knapsack(items: List[Dict[str, Any]], capacity: float) -> Dict[str, Any]:
    steps = []
    
    # Enrich items with ratios
    processed_items = []
    for idx, it in enumerate(items):
        w = float(it["weight"])
        v = float(it["value"])
        name = it.get("name", f"Item {idx + 1}")
        ratio = round(v / w, 2) if w > 0 else 0
        processed_items.append({
            "id": idx + 1,
            "name": name,
            "weight": w,
            "value": v,
            "ratio": ratio,
            "fraction_taken": 0.0,
            "status": "unprocessed"
        })

    def record_step(title: str, explanation: str, line: int, curr_item_idx=None,
                    total_val=0.0, rem_cap=0.0, taking_fraction=None):
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "items": [dict(it) for it in processed_items],
                "capacity": capacity,
                "current_item_index": curr_item_idx,
                "total_value": round(total_val, 2),
                "remaining_capacity": round(rem_cap, 2),
                "used_capacity": round(capacity - rem_cap, 2),
                "taking_fraction": taking_fraction
            },
            "metrics": {
                "capacity_fill_percent": round(((capacity - rem_cap) / capacity) * 100, 1) if capacity > 0 else 0,
                "total_profit": round(total_val, 2),
                "remaining_capacity": round(rem_cap, 2)
            }
        })

    record_step(
        title="Initial Knapsack Problem",
        explanation=f"Given {len(processed_items)} items and bag capacity {capacity}. Computing value-to-weight ratios.",
        line=2,
        total_val=0.0,
        rem_cap=capacity
    )

    # Sort descending by ratio
    processed_items.sort(key=lambda x: x["ratio"], reverse=True)

    record_step(
        title="Sort Items by Ratio (v/w) Descending",
        explanation="Greedy choice property: Always pick the item with the highest density (value per unit weight) first.",
        line=3,
        total_val=0.0,
        rem_cap=capacity
    )

    total_value = 0.0
    remaining_capacity = float(capacity)

    for i, item in enumerate(processed_items):
        item["status"] = "inspecting"
        record_step(
            title=f"Inspect Item '{item['name']}' (Ratio: {item['ratio']})",
            explanation=f"Examining {item['name']}: Weight={item['weight']}, Value={item['value']}. Remaining capacity={remaining_capacity}.",
            line=5,
            curr_item_idx=i,
            total_val=total_value,
            rem_cap=remaining_capacity
        )

        if item["weight"] <= remaining_capacity:
            # Take whole item
            item["fraction_taken"] = 1.0
            item["status"] = "taken_full"
            remaining_capacity -= item["weight"]
            total_value += item["value"]

            record_step(
                title=f"Take 100% of '{item['name']}'",
                explanation=f"Item fits completely! Added weight {item['weight']}, value +{item['value']}. Remaining bag space={remaining_capacity}.",
                line=7,
                curr_item_idx=i,
                total_val=total_value,
                rem_cap=remaining_capacity,
                taking_fraction=1.0
            )

            if remaining_capacity == 0:
                record_step(
                    title="Knapsack Capacity Filled Exactly",
                    explanation="Knapsack is 100% full. Maximum profit reached.",
                    line=11,
                    total_val=total_value,
                    rem_cap=remaining_capacity
                )
                break
        else:
            # Take fractional part
            fraction = remaining_capacity / item["weight"]
            val_added = item["value"] * fraction
            item["fraction_taken"] = round(fraction, 3)
            item["status"] = "taken_fraction"
            total_value += val_added
            remaining_capacity = 0.0

            record_step(
                title=f"Take {round(fraction * 100, 1)}% fraction of '{item['name']}'",
                explanation=f"Bag only has {round(capacity - (capacity - fraction * item['weight']), 2)} space left. Taking fraction {round(fraction, 2)} yielding +{round(val_added, 2)} profit.",
                line=9,
                curr_item_idx=i,
                total_val=total_value,
                rem_cap=0.0,
                taking_fraction=round(fraction, 3)
            )
            break

    # Mark remaining as rejected
    for item in processed_items:
        if item["status"] == "unprocessed":
            item["status"] = "rejected"

    record_step(
        title="Fractional Knapsack Complete",
        explanation=f"Greedy optimization finished. Maximum attainable profit is {round(total_value, 2)}.",
        line=11,
        total_val=total_value,
        rem_cap=remaining_capacity
    )

    return {
        "algorithm": "Fractional Knapsack",
        "paradigm": "Greedy",
        "pseudocode": get_fractional_knapsack_pseudocode(),
        "time_complexity": "O(n log n) due to ratio sorting",
        "space_complexity": "O(1) auxiliary",
        "greedy_choice": "Sorting by Value/Weight ratio guarantees locally optimal choice leads to global optimum for fractional items.",
        "steps": steps,
        "max_value": round(total_value, 2),
        "items": processed_items
    }


def get_activity_selection_pseudocode() -> List[str]:
    return [
        "function activitySelection(activities):",
        "    sort activities by finish_time ascending",
        "    selected = [activities[0]]",
        "    last_finish = activities[0].finish",
        "    for i = 1 to activities.length - 1:",
        "        if activities[i].start >= last_finish: // Non-overlapping",
        "            selected.append(activities[i])",
        "            last_finish = activities[i].finish",
        "    return selected"
    ]


def trace_activity_selection(activities: List[Dict[str, Any]]) -> Dict[str, Any]:
    steps = []
    
    # Prepare activities
    acts = []
    for idx, a in enumerate(activities):
        acts.append({
            "id": a.get("id", f"A{idx + 1}"),
            "name": a.get("name", f"Activity {idx + 1}"),
            "start": int(a["start"]),
            "finish": int(a["finish"]),
            "status": "pending"
        })

    def record_step(title: str, explanation: str, line: int, curr_idx=None, selected_ids=None, last_f=None):
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "activities": [dict(a) for a in acts],
                "current_activity_index": curr_idx,
                "selected_ids": selected_ids or [],
                "last_finish_time": last_f
            },
            "metrics": {
                "selected_count": len(selected_ids or []),
                "total_activities": len(acts)
            }
        })

    record_step(
        title="Initial Activity Set",
        explanation=f"Given {len(acts)} activities with varying start and finish intervals.",
        line=1
    )

    # Sort by finish time ascending
    acts.sort(key=lambda x: x["finish"])

    record_step(
        title="Sort Activities by Finish Time Ascending",
        explanation="Greedy property: Picking the activity that finishes earliest leaves the maximum time available for subsequent activities.",
        line=2
    )

    # Select first activity
    selected = [acts[0]["id"]]
    acts[0]["status"] = "selected"
    last_finish = acts[0]["finish"]

    record_step(
        title=f"Greedily Select First Activity: {acts[0]['id']}",
        explanation=f"Activity {acts[0]['id']} ([{acts[0]['start']}, {acts[0]['finish']}]) finishes earliest. Selected as base.",
        line=3,
        curr_idx=0,
        selected_ids=list(selected),
        last_f=last_finish
    )

    for i in range(1, len(acts)):
        act = acts[i]
        act["status"] = "checking"

        record_step(
            title=f"Check {act['id']} ([{act['start']}, {act['finish']}])",
            explanation=f"Comparing start time ({act['start']}) with current last finish time ({last_finish}).",
            line=6,
            curr_idx=i,
            selected_ids=list(selected),
            last_f=last_finish
        )

        if act["start"] >= last_finish:
            act["status"] = "selected"
            selected.append(act["id"])
            last_finish = act["finish"]

            record_step(
                title=f"Select {act['id']} (Compatible!)",
                explanation=f"{act['start']} >= {last_finish - (act['finish'] - last_finish) if False else 'last finish'}: No conflict! New last finish time is {last_finish}.",
                line=7,
                curr_idx=i,
                selected_ids=list(selected),
                last_f=last_finish
            )
        else:
            act["status"] = "conflict"
            record_step(
                title=f"Reject {act['id']} (Overlaps)",
                explanation=f"Start time {act['start']} is earlier than previous finish time {last_finish}. Conflict detected!",
                line=6,
                curr_idx=i,
                selected_ids=list(selected),
                last_f=last_finish
            )

    record_step(
        title="Activity Selection Complete",
        explanation=f"Greedy algorithm scheduled {len(selected)} non-conflicting activities maximally.",
        line=9,
        selected_ids=list(selected),
        last_f=last_finish
    )

    return {
        "algorithm": "Activity Selection / Interval Scheduling",
        "paradigm": "Greedy",
        "pseudocode": get_activity_selection_pseudocode(),
        "time_complexity": "O(n log n) sorting + O(n) scan = O(n log n)",
        "space_complexity": "O(1) auxiliary",
        "greedy_choice": "Earliest Finish Time First (EFF) ensures maximal compatibility interval.",
        "steps": steps,
        "selected_activities": selected,
        "activities": acts
    }


def get_dijkstra_pseudocode() -> List[str]:
    return [
        "function dijkstra(graph, source):",
        "    dist = [infinity for each node]; dist[source] = 0",
        "    pq = MinPriorityQueue(); pq.push((0, source))",
        "    while pq is not empty:",
        "        (d, u) = pq.pop()",
        "        if d > dist[u]: continue",
        "        for each neighbor v of u with weight w:",
        "            if dist[u] + w < dist[v]:  // Edge Relaxation",
        "                dist[v] = dist[u] + w",
        "                pq.push((dist[v], v))",
        "    return dist"
    ]


def trace_dijkstra(graph_data: Dict[str, Any], source: str) -> Dict[str, Any]:
    nodes = graph_data.get("nodes", ["A", "B", "C", "D", "E"])
    edges = graph_data.get("edges", [
        {"from": "A", "to": "B", "weight": 4},
        {"from": "A", "to": "C", "weight": 2},
        {"from": "B", "to": "C", "weight": 1},
        {"from": "B", "to": "D", "weight": 5},
        {"from": "C", "to": "D", "weight": 8},
        {"from": "C", "to": "E", "weight": 10},
        {"from": "D", "to": "E", "weight": 2}
    ])

    adj = {n: [] for n in nodes}
    for e in edges:
        adj[e["from"]].append((e["to"], e["weight"]))
        # Undirected if specified or directed
        if graph_data.get("undirected", True):
            adj[e["to"]].append((e["from"], e["weight"]))

    dist = {n: float("inf") for n in nodes}
    dist[source] = 0
    parent = {n: None for n in nodes}
    visited = set()
    pq = [(0, source)]

    steps = []

    def record_step(title: str, explanation: str, line: int, curr_u=None,
                    active_edge=None, relaxed_edge=None):
        clean_dist = {k: ("inf" if v == float("inf") else v) for k, v in dist.items()}
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "nodes": nodes,
                "edges": edges,
                "distances": clean_dist,
                "visited": list(visited),
                "current_node": curr_u,
                "active_edge": active_edge,
                "relaxed_edge": relaxed_edge,
                "parents": dict(parent),
                "priority_queue": [(d, u) for d, u in sorted(pq)]
            },
            "metrics": {
                "visited_count": len(visited),
                "unvisited_count": len(nodes) - len(visited)
            }
        })

    record_step(
        title=f"Initialize Distances from Source '{source}'",
        explanation=f"Set dist[{source}] = 0, all other vertices dist[v] = ∞. Added {source} to Min-Heap.",
        line=2
    )

    while pq:
        d, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)
        record_step(
            title=f"Extract Min Vertex: '{u}' with dist={d}",
            explanation=f"Greedy choice: Node '{u}' has the smallest unfinalized provisional distance ({d}). Finalizing '{u}'.",
            line=5,
            curr_u=u
        )

        for neighbor, weight in adj[u]:
            record_step(
                title=f"Inspect Edge ({u} -> {neighbor}) with weight={weight}",
                explanation=f"Checking if path through '{u}' improves distance to '{neighbor}' (current dist: {dist[neighbor]}).",
                line=7,
                curr_u=u,
                active_edge={"from": u, "to": neighbor, "weight": weight}
            )

            if dist[u] + weight < dist[neighbor]:
                old_d = dist[neighbor]
                dist[neighbor] = dist[u] + weight
                parent[neighbor] = u
                heapq.heappush(pq, (dist[neighbor], neighbor))

                record_step(
                    title=f"Relax Edge ({u} -> {neighbor}): New dist={dist[neighbor]}",
                    explanation=f"Relaxation: dist[{neighbor}] decreased from {('∞' if old_d == float('inf') else old_d)} to {dist[neighbor]} via '{u}'.",
                    line=9,
                    curr_u=u,
                    relaxed_edge={"from": u, "to": neighbor, "weight": weight}
                )

    clean_dist = {k: ("inf" if v == float("inf") else v) for k, v in dist.items()}
    record_step(
        title="Dijkstra Algorithm Complete",
        explanation="All reachable vertices processed. Optimal shortest path tree constructed.",
        line=11
    )

    return {
        "algorithm": "Dijkstra's Shortest Path",
        "paradigm": "Greedy",
        "pseudocode": get_dijkstra_pseudocode(),
        "time_complexity": "O((V + E) log V) with Min-Heap",
        "space_complexity": "O(V) for distances and queue",
        "greedy_choice": "Always finalizes the vertex with minimum provisional distance, exploiting non-negative edge weights.",
        "steps": steps,
        "distances": clean_dist,
        "parents": parent
    }


def get_huffman_pseudocode() -> List[str]:
    return [
        "function huffmanCoding(frequencies):",
        "    pq = MinPriorityQueue() // Insert leaf nodes",
        "    while pq.size() > 1:",
        "        left = pq.popMin()",
        "        right = pq.popMin()",
        "        parent = Node(freq = left.freq + right.freq, left, right)",
        "        pq.push(parent)",
        "    return pq.popMin() // Root of Huffman Tree"
    ]


def trace_huffman_coding(char_freqs: Dict[str, int]) -> Dict[str, Any]:
    steps = []
    
    # Create initial priority queue
    counter = 0
    pq = []
    for char, freq in char_freqs.items():
        node = {
            "id": f"node_{counter}",
            "char": char,
            "freq": freq,
            "left": None,
            "right": None,
            "is_leaf": True
        }
        counter += 1
        # Store as (freq, counter, node) for stable comparison
        heapq.heappush(pq, (freq, counter, node))

    all_nodes = [item[2] for item in pq]

    def record_step(title: str, explanation: str, line: int, merging=None, created_node=None):
        current_pq_display = [{"char": it[2]["char"], "freq": it[0], "id": it[2]["id"]} for it in sorted(pq)]
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "all_nodes": [dict(n) for n in all_nodes],
                "priority_queue": current_pq_display,
                "merging_nodes": merging or [],
                "new_node": created_node
            },
            "metrics": {
                "queue_size": len(pq),
                "nodes_count": len(all_nodes)
            }
        })

    record_step(
        title="Initialize Huffman Priority Queue",
        explanation=f"Created {len(char_freqs)} leaf nodes sorted by ascending character frequencies.",
        line=2
    )

    while len(pq) > 1:
        f1, _, left_node = heapq.heappop(pq)
        f2, _, right_node = heapq.heappop(pq)

        record_step(
            title=f"Extract Two Smallest: '{left_node['char']}' ({f1}) & '{right_node['char']}' ({f2})",
            explanation=f"Greedy choice: Combine the two lowest frequency subtrees to keep overall weighted path length minimal.",
            line=4,
            merging=[left_node["id"], right_node["id"]]
        )

        counter += 1
        merged_char = f"{left_node['char']}+{right_node['char']}"
        parent_node = {
            "id": f"node_{counter}",
            "char": merged_char,
            "freq": f1 + f2,
            "left": left_node["id"],
            "right": right_node["id"],
            "is_leaf": False
        }
        all_nodes.append(parent_node)
        heapq.heappush(pq, (parent_node["freq"], counter, parent_node))

        record_step(
            title=f"Merged into Parent with Freq={parent_node['freq']}",
            explanation=f"Created interior node with left branch (code '0') and right branch (code '1'). Re-inserted into min-heap.",
            line=6,
            created_node=parent_node
        )

    root = pq[0][2]

    # Generate codes
    codes = {}
    def generate_codes(node_id, current_code):
        node = next(n for n in all_nodes if n["id"] == node_id)
        if node["is_leaf"]:
            codes[node["char"]] = current_code or "0"
            return
        if node["left"]:
            generate_codes(node["left"], current_code + "0")
        if node["right"]:
            generate_codes(node["right"], current_code + "1")

    generate_codes(root["id"], "")

    record_step(
        title="Huffman Tree Construction Complete",
        explanation=f"Prefix-free optimal binary tree generated. Total unique codes: {len(codes)}.",
        line=8
    )

    return {
        "algorithm": "Huffman Coding",
        "paradigm": "Greedy",
        "pseudocode": get_huffman_pseudocode(),
        "time_complexity": "O(n log n) where n is alphabet size",
        "space_complexity": "O(n) for tree storage",
        "greedy_choice": "Merging the two lowest frequency subtrees at each step is proven to generate optimal prefix codes.",
        "steps": steps,
        "tree_nodes": all_nodes,
        "root_id": root["id"],
        "huffman_codes": codes
    }


def get_job_sequencing_pseudocode() -> List[str]:
    return [
        "function jobSequencing(jobs):",
        "    sort jobs by profit descending",
        "    slots = [empty for 1 to max_deadline]",
        "    for job in jobs:",
        "        for slot = min(max_deadline, job.deadline) down to 1:",
        "            if slots[slot] is empty:",
        "                slots[slot] = job; total_profit += job.profit; break",
        "    return slots"
    ]


def trace_job_sequencing(jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
    steps = []
    
    # Process jobs
    job_list = []
    for idx, j in enumerate(jobs):
        job_list.append({
            "id": j.get("id", f"J{idx + 1}"),
            "deadline": int(j["deadline"]),
            "profit": int(j["profit"]),
            "status": "pending"
        })

    max_deadline = max(j["deadline"] for j in job_list) if job_list else 1
    # Slots 1 to max_deadline
    slots = [None] * (max_deadline + 1)
    total_profit = 0

    def record_step(title: str, explanation: str, line: int, curr_job_idx=None, checked_slot=None):
        slot_display = [{"slot": s, "job": slots[s]} for s in range(1, max_deadline + 1)]
        steps.append({
            "step_number": len(steps) + 1,
            "title": title,
            "explanation": explanation,
            "pseudocode_line": line,
            "state": {
                "jobs": [dict(j) for j in job_list],
                "current_job_index": curr_job_idx,
                "slots": slot_display,
                "checked_slot": checked_slot,
                "total_profit": total_profit
            },
            "metrics": {
                "total_profit": total_profit,
                "scheduled_jobs": len([s for s in slots if s is not None])
            }
        })

    record_step(
        title="Initial Jobs Set",
        explanation=f"Given {len(job_list)} jobs with deadlines and profits. Max deadline is {max_deadline}.",
        line=1
    )

    # Sort by profit descending
    job_list.sort(key=lambda x: x["profit"], reverse=True)

    record_step(
        title="Sort Jobs by Profit Descending",
        explanation="Greedy property: Prioritize highest-paying jobs first, placing each into the latest possible available slot before its deadline.",
        line=2
    )

    for i, job in enumerate(job_list):
        job["status"] = "inspecting"
        record_step(
            title=f"Inspect Job {job['id']} (Profit: {job['profit']}, Deadline: {job['deadline']})",
            explanation=f"Searching for an available timeline slot from {min(max_deadline, job['deadline'])} down to 1.",
            line=4,
            curr_job_idx=i
        )

        placed = False
        for slot in range(min(max_deadline, job["deadline"]), 0, -1):
            if slots[slot] is None:
                slots[slot] = job["id"]
                total_profit += job["profit"]
                job["status"] = "scheduled"
                placed = True
                record_step(
                    title=f"Assign {job['id']} to Slot {slot}",
                    explanation=f"Slot {slot} was free! Job {job['id']} scheduled, earning profit +{job['profit']}.",
                    line=6,
                    curr_job_idx=i,
                    checked_slot=slot
                )
                break
            else:
                record_step(
                    title=f"Slot {slot} Occupied by {slots[slot]}",
                    explanation=f"Slot {slot} already occupied. Checking earlier slot {slot - 1}...",
                    line=5,
                    curr_job_idx=i,
                    checked_slot=slot
                )

        if not placed:
            job["status"] = "dropped"
            record_step(
                title=f"Drop Job {job['id']}",
                explanation=f"No free slots found before deadline {job['deadline']}. Job {job['id']} cannot be completed.",
                line=4,
                curr_job_idx=i
            )

    record_step(
        title="Job Sequencing Complete",
        explanation=f"All jobs evaluated. Maximum profit obtained: {total_profit}.",
        line=8
    )

    return {
        "algorithm": "Job Sequencing with Deadlines",
        "paradigm": "Greedy",
        "pseudocode": get_job_sequencing_pseudocode(),
        "time_complexity": "O(n²), can be optimized to O(n log n) with Disjoint Set Union (DSU)",
        "space_complexity": "O(max_deadline)",
        "greedy_choice": "Sorting by profit and greedily booking the latest valid slot preserves earlier slots for jobs with tighter deadlines.",
        "steps": steps,
        "total_profit": total_profit,
        "schedule": [{"slot": s, "job": slots[s]} for s in range(1, max_deadline + 1)]
    }
