"""
Routes Package Init
"""

from .trace import router as trace_router
from .ai import router as ai_router

__all__ = ["trace_router", "ai_router"]
