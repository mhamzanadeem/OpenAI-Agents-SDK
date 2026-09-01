"""
Main AI Research & Report Agent.

Architecture:

    Research Agent
          |
          | web_search
          | calculate_statistics
          |
          | research complete
          v
        HANDOFF
          |
          v
    Report Writer Agent
          |
          | calculate_statistics
          | save_report
          |
          v
      Final Report
"""

from __future__ import annotations

import asyncio
import logging
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    RunConfig,
    handoff,
    set_tracing_disabled,
)

from tools import (
    calculate_statistics,
    save_report,
    web_search,
)


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=getattr(
        logging,
        os.getenv(
            "LOG_LEVEL",
            "INFO",
        ).upper(),
        logging.INFO,
    ),
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger(
    "ai-research-agent"
)


# ============================================================
# CONFIGURATION
# ============================================================

PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "openai",
).lower()

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini",
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

MAX_AGENT_RETRIES = int(
    os.getenv(
        "MAX_RETRIES",
        "4",
    )
)


# ============================================================
# MODEL CREATION
# ============================================================

def build_model():
    """
    Build the model configuration for either OpenAI or Groq.
    """

    if PROVIDER == "groq":

        api_key = os.getenv(
            "GROQ_API_KEY"
        )

        if not api_key:

            raise RuntimeError(
                "GROQ_API_KEY is required "
                "when LLM_PROVIDER=groq"
            )

        # Disable OpenAI tracing for Groq.
        set_tracing_disabled(True)

        client = AsyncOpenAI(
            api_key=api_key,
            base_url=(
                "https://api.groq.com/openai/v1"
            ),
        )

        return OpenAIChatCompletionsModel(
            model=GROQ_MODEL,
            openai_client=client,
        )

    if PROVIDER == "openai":

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:

            raise RuntimeError(
                "OPENAI_API_KEY is required "
                "when LLM_PROVIDER=openai"
            )

        client = AsyncOpenAI(
            api_key=api_key,
        )

        return OpenAIChatCompletionsModel(
            model=OPENAI_MODEL,
            openai_client=client,
        )

    raise RuntimeError(
        "LLM_PROVIDER must be either "
        "'openai' or 'groq'"
    )


MODEL = build_model()


# ============================================================
# REPORT WRITER AGENT
# ============================================================

report_writer_agent = Agent(
    name="Report Writer Agent",

    handoff_description=(
        "Specialist responsible for turning completed "
        "research into a structured executive report."
    ),

    model=MODEL,

    instructions="""
You are the Report Writer Agent.

You receive the complete research conversation from
the Research Agent.

Your responsibility is to turn the research into a
professional, structured Markdown report.

IMPORTANT:

Do not invent facts.

Clearly distinguish:

1. Directly sourced facts
2. Calculated values
3. Analytical estimates
4. Assumptions

The report must contain:

# AI Trends 2024 Research Report

## 1. Executive Summary

Summarize the five most important findings.

## 2. Top 5 Emerging AI Trends

For each trend include:

- Trend name
- Why it emerged in 2024
- Supporting evidence
- Potential market impact
- Estimated investment required
- Investment estimate rationale
- Sources

## 3. Investment Analysis

Create a table:

| Trend | Estimated Investment |
|------|----------------------|

Then provide:

- Total estimated investment
- Average investment
- Minimum investment
- Maximum investment

The average MUST be calculated using the
calculate_statistics tool if numerical estimates
are available.

## 4. Market Impact

Explain the likely impact on:

- Enterprise software
- Infrastructure
- Labor/productivity
- Cybersecurity
- Consumer technology
- Capital markets

## 5. Risks and Assumptions

Clearly explain uncertainty.

## 6. Conclusion

Provide a concise investment and strategic conclusion.

## Sources

List URLs used by the research.

The final output must be Markdown.
""",

    tools=[
        calculate_statistics,
        save_report,
    ],
)


# ============================================================
# RESEARCH AGENT
# ============================================================

research_agent = Agent(
    name="Research Agent",

    handoff_description=(
        "Research specialist that gathers evidence, "
        "analyzes trends, calculates investment estimates, "
        "and hands completed research to the Report Writer."
    ),

    model=MODEL,

    instructions="""
You are the Research Agent.

Your job is to independently research the user's
question and prepare a high-quality research dataset.

The primary task is:

"Research the top 5 emerging AI trends in 2024,
analyze their potential market impact, calculate
average investment needed, and generate a structured report."

You MUST perform multiple research steps.

============================================================
STEP 1 — IDENTIFY THE FIVE TRENDS
============================================================

Identify five genuinely important emerging AI trends
from 2024.

Do not simply repeat generic categories.

Possible examples include:

- Generative AI
- AI agents
- AI infrastructure
- Edge/on-device AI
- AI cybersecurity

But select the strongest five based on evidence.

============================================================
STEP 2 — WEB RESEARCH
============================================================

Use web_search multiple times.

Search separately for:

1. Overall AI trends in 2024
2. Trend #1 evidence
3. Trend #2 evidence
4. Trend #3 evidence
5. Trend #4 evidence
6. Trend #5 evidence
7. Market impact
8. Investment/capital requirements

Prefer authoritative sources.

Look for:

- Government publications
- Major research organizations
- Company filings
- Major technology companies
- Industry reports
- Reputable financial publications
- Academic research
- Credible market research

Do not rely on a single source.

============================================================
STEP 3 — EVIDENCE
============================================================

For each trend collect:

- trend
- evidence
- source URL
- source title
- market impact
- investment estimate
- investment estimate rationale

============================================================
STEP 4 — INVESTMENT ESTIMATES
============================================================

Estimate the investment required to meaningfully
participate in or build capability around each trend.

Use USD millions.

IMPORTANT:

If a source provides an actual investment number,
use it and cite it.

If a direct investment figure is unavailable,
produce an analytical estimate.

Clearly label analytical estimates.

Do NOT pretend estimates are sourced facts.

============================================================
STEP 5 — CALCULATION
============================================================

After obtaining five numerical investment estimates,
call:

calculate_statistics

with:

metric = "mean"

Also calculate:

- sum
- minimum
- maximum

The average investment is mandatory.

============================================================
STEP 6 — QUALITY CHECK
============================================================

Before handing off, verify:

- exactly five trends
- each trend has evidence
- each trend has source URLs
- each trend has market impact
- each trend has investment estimate
- average investment calculated
- assumptions identified

============================================================
STEP 7 — HANDOFF
============================================================

When the research dataset is complete:

IMMEDIATELY hand off to the Report Writer Agent.

Do NOT write the final report yourself.

The Report Writer Agent owns the final response.
""",

    tools=[
        web_search,
        calculate_statistics,
    ],

    handoffs=[
        handoff(report_writer_agent)
    ],
)


# ============================================================
# RETRYABLE AGENT RUN
# ============================================================

async def run_agent_with_retries(
    prompt: str,
    max_attempts: int = MAX_AGENT_RETRIES,
):
    """
    Run the complete agent workflow with retries
    for common transient provider errors.
    """

    last_error: Optional[Exception] = None

    for attempt in range(max_attempts):

        try:

            logger.info(
                "Starting agent run. Attempt %s/%s",
                attempt + 1,
                max_attempts,
            )

            result = await Runner.run(
                research_agent,
                prompt,
                run_config=RunConfig(
                    tracing_disabled=(
                        PROVIDER == "groq"
                    ),
                ),
            )

            logger.info(
                "Agent workflow completed. "
                "Final agent: %s",
                result.last_agent.name,
            )

            return result

        except Exception as exc:

            last_error = exc

            error_text = str(exc).lower()

            retryable = any(
                phrase in error_text
                for phrase in [
                    "rate limit",
                    "429",
                    "timeout",
                    "timed out",
                    "temporarily unavailable",
                    "502",
                    "503",
                    "504",
                    "connection reset",
                ]
            )

            if not retryable:

                logger.exception(
                    "Non-retryable agent failure."
                )

                raise

            if attempt >= max_attempts - 1:

                logger.exception(
                    "Agent failed after maximum retries."
                )

                raise

            delay = min(
                2 ** attempt,
                16,
            )

            logger.warning(
                "Transient failure. "
                "Retrying in %s seconds.",
                delay,
            )

            await asyncio.sleep(delay)

    raise last_error or RuntimeError(
        "Agent workflow failed"
    )


# ============================================================
# PUBLIC APPLICATION FUNCTION
# ============================================================

async def run_research_report(
    user_task: Optional[str] = None,
) -> str:
    """
    Run the full Research -> Handoff -> Report workflow.
    """

    task = user_task or (
        "Research the top 5 emerging AI trends in 2024, "
        "analyze their potential market impact, "
        "calculate average investment needed, "
        "and generate a structured report."
    )

    result = await run_agent_with_retries(
        task
    )

    return result.final_output


# ============================================================
# CLI ENTRY POINT
# ============================================================

if __name__ == "__main__":

    default_task = (
        "Research the top 5 emerging AI trends in 2024, "
        "analyze their potential market impact, "
        "calculate average investment needed, "
        "and generate a structured report."
    )

    final_report = asyncio.run(
        run_research_report(
            default_task
        )
    )

    print()
    print("=" * 80)
    print("FINAL RESEARCH REPORT")
    print("=" * 80)
    print()
    print(final_report)