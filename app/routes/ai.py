"""
FastAPI Routes for AI Algorithm Assistance
"""

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from app.ai.engine import ai_engine
from app.ai.prompt_templates import EXPERT_PARADIGM_KNOWLEDGE

router = APIRouter(prefix="/api/ai", tags=["AI Assistance"])


class ExplainStepRequest(BaseModel):
    algorithm: str
    paradigm: str
    step: Dict[str, Any]


class DetectParadigmRequest(BaseModel):
    problem_text: str


class MasterTheoremRequest(BaseModel):
    a: float
    b: float
    k: float
    p: Optional[float] = 0.0


class TestcaseRequest(BaseModel):
    algorithm: str
    case_type: Optional[str] = "random"


@router.post("/explain-step")
async def explain_step_endpoint(req: ExplainStepRequest, x_gemini_key: Optional[str] = Header(None)):
    try:
        result = ai_engine.explain_step(
            algorithm=req.algorithm,
            paradigm=req.paradigm,
            step_data=req.step,
            custom_key=x_gemini_key
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect-paradigm")
async def detect_paradigm_endpoint(req: DetectParadigmRequest, x_gemini_key: Optional[str] = Header(None)):
    if not req.problem_text or len(req.problem_text.strip()) < 5:
        raise HTTPException(status_code=400, detail="Please enter a meaningful problem description.")
    try:
        result = ai_engine.detect_paradigm(req.problem_text.strip(), custom_key=x_gemini_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/master-theorem")
async def master_theorem_endpoint(req: MasterTheoremRequest):
    if req.a < 1:
        raise HTTPException(status_code=400, detail="Parameter 'a' must be >= 1 (number of subproblems).")
    if req.b <= 1:
        raise HTTPException(status_code=400, detail="Parameter 'b' must be > 1 (subproblem factor division).")
    if req.k < 0:
        raise HTTPException(status_code=400, detail="Parameter 'k' must be >= 0.")

    result = ai_engine.solve_master_theorem(req.a, req.b, req.k, req.p or 0.0)
    return result


@router.post("/generate-testcase")
async def testcase_endpoint(req: TestcaseRequest):
    return ai_engine.generate_testcase(req.algorithm, req.case_type or "random")


@router.get("/paradigm-knowledge")
async def paradigm_knowledge():
    return EXPERT_PARADIGM_KNOWLEDGE


@router.get("/preset-problems")
async def preset_problems():
    return [
        {
            "title": "Continuous Metal Smelting (Knapsack with Split)",
            "problem": "A thief enters a jewelry warehouse with a 50kg bag. He finds barrels of Gold dust, Silver flakes, and Platinum powder with specific weights and values. He can take any fraction of a barrel. How should he maximize profit?",
            "paradigm": "Greedy",
            "algo": "fractional_knapsack"
        },
        {
            "title": "Discrete Luggage Packing (0/1 Knapsack)",
            "problem": "An astronaut has an 8kg payload limit and must select whole pieces of scientific equipment. Each device cannot be split into pieces. How to select the equipment subset to maximize scientific value?",
            "paradigm": "Dynamic Programming",
            "algo": "knapsack01"
        },
        {
            "title": "Conference Room Booking (Interval Scheduling)",
            "problem": "A university has a single auditorium and 8 student clubs requesting meeting times with start and finish hours. What is the maximum number of non-overlapping meetings that can be scheduled?",
            "paradigm": "Greedy",
            "algo": "activity_selection"
        },
        {
            "title": "DNA Sequence Homology Alignment (LCS)",
            "problem": "Biologists are comparing two genomic strands: S1 = 'AGGTAB' and S2 = 'GXTXAYB'. Find the longest sequence of nucleotides that appears in both strands in the exact same relative order without mutating.",
            "paradigm": "Dynamic Programming",
            "algo": "lcs"
        },
        {
            "title": "Fast Recursive Array Sorting (Merge Sort)",
            "problem": "Sort a large dataset of customer records by age in guaranteed O(n log n) worst-case time by dividing the list in half recursively and merging the sorted parts.",
            "paradigm": "Divide and Conquer",
            "algo": "merge_sort"
        },
        {
            "title": "Minimum Vending Machine Dispense (Coin Change)",
            "problem": "A vending machine must return 11 units of change using coins of denominations [1, 2, 5]. What is the minimum count of coins needed to dispense the exact change?",
            "paradigm": "Dynamic Programming",
            "algo": "coin_change"
        },
        {
            "title": "Shortest Optical Fiber Network Route (Dijkstra)",
            "problem": "Given a network of 5 servers connected by fiber optic cables with transmission delays, find the fastest route from server A to all other servers.",
            "paradigm": "Greedy",
            "algo": "dijkstra"
        }
    ]
