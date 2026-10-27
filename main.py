"""
AI-Based Visualization of Divide-and-Conquer, Greedy and Dynamic Programming Algorithms
FastAPI Backend & Web Application Server
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routes import trace_router, ai_router

app = FastAPI(
    title="AI-Based DAA Algorithm Visualizer",
    description="Interactive visualizer and AI tutor for Divide-and-Conquer, Greedy, and Dynamic Programming algorithms.",
    version="1.0.0"
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(trace_router)
app.include_router(ai_router)

# Mount static directory for CSS, JS, Assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "AI-Based DAA Visualizer",
        "version": "1.0.0",
        "paradigms": ["Divide-and-Conquer", "Greedy", "Dynamic Programming"]
    }


@app.get("/")
async def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "DAA Visualizer API is running. index.html not found yet in static/."}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"Starting AI DAA Visualizer server at http://localhost:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
