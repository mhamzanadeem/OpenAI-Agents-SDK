"""
FastAPI HTTP interface for the AI Research Agent.
"""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import run_research_report


logger = logging.getLogger(
    "research-api"
)


app = FastAPI(
    title="AI Research & Report Agent",
    description=(
        "Multi-agent research system using "
        "the OpenAI Agents SDK."
    ),
    version="1.0.0",
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ResearchRequest(BaseModel):

    task: str = Field(
        default=(
            "Research the top 5 emerging AI trends "
            "in 2024, analyze their potential market "
            "impact, calculate average investment needed, "
            "and generate a structured report."
        ),
        min_length=10,
        max_length=10000,
    )


# ============================================================
# RESPONSE MODEL
# ============================================================

class ResearchResponse(BaseModel):

    report: str


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "provider": os.getenv(
            "LLM_PROVIDER",
            "openai",
        ),
    }


# ============================================================
# RESEARCH ENDPOINT
# ============================================================

@app.post(
    "/research",
    response_model=ResearchResponse,
)
async def research(
    request: ResearchRequest,
):

    try:

        report = await run_research_report(
            request.task
        )

        return ResearchResponse(
            report=report
        )

    except Exception as exc:

        logger.exception(
            "Research endpoint failed."
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "The AI research workflow failed. "
                "Check server logs."
            ),
        ) from exc