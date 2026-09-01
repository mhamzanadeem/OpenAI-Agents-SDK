"""
Tools used by the AI Research & Report Agent.

Tools:
    1. web_search
    2. calculate_statistics
    3. save_report

The web search tool uses Tavily when TAVILY_API_KEY is configured.
Otherwise it falls back to a deterministic simulator.
"""

from __future__ import annotations

import asyncio
import json
import logging
import math
import os
import random
from statistics import mean, median
from typing import Any, Callable, Awaitable

import httpx
from agents import function_tool


logger = logging.getLogger(__name__)


# ============================================================
# CONFIGURATION
# ============================================================

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", "4")
)

REQUEST_TIMEOUT = float(
    os.getenv("REQUEST_TIMEOUT_SECONDS", "30")
)


# ============================================================
# SIMULATED SEARCH DATA
# ============================================================

SIMULATED_RESULTS = [
    {
        "title": "Generative AI and Foundation Models",
        "url": "https://example.com/generative-ai",
        "content": (
            "Generative AI became one of the most significant technology "
            "trends in 2024. Foundation models enabled applications in "
            "software development, enterprise search, content creation, "
            "customer service, and knowledge work."
        ),
    },
    {
        "title": "AI Agents and Autonomous Workflows",
        "url": "https://example.com/ai-agents",
        "content": (
            "AI agents emerged as a major 2024 trend as models became "
            "capable of planning, tool usage, multi-step reasoning, and "
            "execution of business workflows."
        ),
    },
    {
        "title": "AI Infrastructure and Accelerators",
        "url": "https://example.com/ai-infrastructure",
        "content": (
            "AI infrastructure experienced significant investment in "
            "GPUs, accelerators, networking, data centers, cloud capacity, "
            "model serving, and inference infrastructure."
        ),
    },
    {
        "title": "Edge AI and On-Device Intelligence",
        "url": "https://example.com/edge-ai",
        "content": (
            "Smaller models and increasingly capable edge processors "
            "enabled AI workloads directly on smartphones, PCs, vehicles, "
            "industrial systems, and other devices."
        ),
    },
    {
        "title": "AI Cybersecurity",
        "url": "https://example.com/ai-security",
        "content": (
            "AI cybersecurity became increasingly important as organizations "
            "used AI to detect threats while simultaneously dealing with "
            "new risks associated with AI applications and models."
        ),
    },
]


# ============================================================
# GENERIC RETRY FUNCTION
# ============================================================

async def with_exponential_backoff(
    operation: Callable[[], Awaitable[Any]],
    operation_name: str,
):
    """
    Execute an async operation with exponential backoff.

    Retries:
        - timeouts
        - network errors
        - HTTP 408
        - HTTP 425
        - HTTP 429
        - HTTP 5xx
    """

    last_error = None

    for attempt in range(MAX_RETRIES + 1):

        try:

            return await operation()

        except (
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError,
        ) as exc:

            last_error = exc

            response = getattr(exc, "response", None)

            status_code = (
                response.status_code
                if response is not None
                else None
            )

            retryable = (
                status_code is None
                or status_code in (408, 425, 429)
                or status_code >= 500
            )

            if not retryable:

                logger.exception(
                    "%s failed with non-retryable error",
                    operation_name,
                )

                raise

            if attempt >= MAX_RETRIES:

                logger.exception(
                    "%s failed after maximum retries",
                    operation_name,
                )

                raise

            delay = min(
                2 ** attempt + random.random(),
                20,
            )

            logger.warning(
                "%s failed on attempt %s/%s. "
                "Retrying in %.2f seconds.",
                operation_name,
                attempt + 1,
                MAX_RETRIES + 1,
                delay,
            )

            await asyncio.sleep(delay)

    raise last_error or RuntimeError(
        f"{operation_name} failed"
    )


# ============================================================
# TAVILY SEARCH
# ============================================================

async def tavily_search(
    query: str,
    max_results: int,
) -> list[dict[str, Any]]:

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:

        logger.warning(
            "TAVILY_API_KEY not configured. "
            "Using simulated search results."
        )

        return SIMULATED_RESULTS[:max_results]

    async def request():

        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT
        ) as client:

            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": api_key,
                    "query": query,
                    "search_depth": "advanced",
                    "max_results": max_results,
                    "include_answer": True,
                    "include_raw_content": False,
                },
            )

            response.raise_for_status()

            return response.json()

    data = await with_exponential_backoff(
        request,
        "Tavily search",
    )

    results = []

    for item in data.get("results", []):

        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
            }
        )

    return results


# ============================================================
# TOOL 1: WEB SEARCH
# ============================================================

@function_tool
async def web_search(
    query: str,
    max_results: int = 5,
) -> str:
    """
    Search the web for research evidence.

    Args:
        query:
            A focused research query.

        max_results:
            Number of search results to return.
            Maximum is 10.
    """

    max_results = max(
        1,
        min(max_results, 10),
    )

    logger.info(
        "Web search requested: %s",
        query,
    )

    try:

        results = await tavily_search(
            query=query,
            max_results=max_results,
        )

        return json.dumps(
            {
                "query": query,
                "results": results,
            },
            ensure_ascii=False,
        )

    except Exception as exc:

        logger.exception(
            "Web search failed. Continuing gracefully."
        )

        return json.dumps(
            {
                "query": query,
                "results": [],
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }
        )


# ============================================================
# TOOL 2: DATA ANALYSIS
# ============================================================

@function_tool
def calculate_statistics(
    values: list[float],
    metric: str = "mean",
) -> str:
    """
    Calculate statistics over numeric values.

    Args:
        values:
            List of numeric values.

        metric:
            mean
            median
            min
            max
            sum

    Values are interpreted as USD millions by the research workflow.
    """

    if not values:

        raise ValueError(
            "values cannot be empty"
        )

    numeric_values = [
        float(value)
        for value in values
    ]

    if not all(
        math.isfinite(value)
        for value in numeric_values
    ):

        raise ValueError(
            "values must contain only finite numbers"
        )

    metric = metric.lower().strip()

    if metric == "mean":

        result = mean(
            numeric_values
        )

    elif metric == "median":

        result = median(
            numeric_values
        )

    elif metric == "min":

        result = min(
            numeric_values
        )

    elif metric == "max":

        result = max(
            numeric_values
        )

    elif metric == "sum":

        result = sum(
            numeric_values
        )

    else:

        raise ValueError(
            "metric must be one of: "
            "mean, median, min, max, sum"
        )

    output = {
        "metric": metric,
        "values": numeric_values,
        "result": round(
            float(result),
            2,
        ),
        "units": "USD millions",
    }

    logger.info(
        "Calculated %s over %s -> %s",
        metric,
        numeric_values,
        result,
    )

    return json.dumps(output)


# ============================================================
# OPTIONAL FILE TOOL
# ============================================================

@function_tool
def save_report(
    report: str,
    filename: str = "research_report.md",
) -> str:
    """
    Save a Markdown report to the reports directory.

    Args:
        report:
            Markdown report contents.

        filename:
            Output filename.
    """

    # Prevent path traversal.
    safe_filename = os.path.basename(
        filename
    )

    if not safe_filename.endswith(".md"):

        safe_filename += ".md"

    reports_directory = os.path.join(
        os.getcwd(),
        "reports",
    )

    os.makedirs(
        reports_directory,
        exist_ok=True,
    )

    output_path = os.path.join(
        reports_directory,
        safe_filename,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(report)

    logger.info(
        "Report saved to %s",
        output_path,
    )

    return json.dumps(
        {
            "saved": True,
            "path": output_path,
        }
    )