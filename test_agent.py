"""
Tests for the AI Research Agent.

These tests do not require an LLM API call.
"""

import json
import os

from tools import (
    SIMULATED_RESULTS,
    calculate_statistics,
)


def test_mean():

    result = json.loads(
        calculate_statistics.__wrapped__(
            [100, 200, 300, 400, 500]
        )
    )

    assert result["metric"] == "mean"

    assert result["result"] == 300.0


def test_sum():

    result = json.loads(
        calculate_statistics.__wrapped__(
            [100, 200, 300],
            "sum",
        )
    )

    assert result["result"] == 600.0


def test_min():

    result = json.loads(
        calculate_statistics.__wrapped__(
            [100, 200, 300],
            "min",
        )
    )

    assert result["result"] == 100.0


def test_max():

    result = json.loads(
        calculate_statistics.__wrapped__(
            [100, 200, 300],
            "max",
        )
    )

    assert result["result"] == 300.0


def test_median():

    result = json.loads(
        calculate_statistics.__wrapped__(
            [100, 200, 500, 800],
            "median",
        )
    )

    assert result["result"] == 350.0


def test_simulated_search_dataset():

    assert len(
        SIMULATED_RESULTS
    ) >= 5


def test_env_file_template_exists():

    assert os.path.exists(
        ".env.example"
    )