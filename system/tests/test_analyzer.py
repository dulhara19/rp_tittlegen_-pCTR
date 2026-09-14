"""Automated Sprint 2 checks (PLAN_IMPLEMENTATION.md §2.6 exit criteria).

Runs the Analyzer against 10 synthetic transcripts and checks schema
conformance + basic sanity bounds. Factual-accuracy / no-invented-entities
verification is inherently manual — see manual_check_analyzer.py.

Requires OPENAI_API_KEY (system/.env) and makes real API calls.
"""

import re

import pytest

from system.agents import analyzer
from system.agents.schemas import VideoBrief
from system.tests.fixtures import TEST_VIDEO_INPUTS

HAS_ENTITY_SIGNAL = re.compile(r"\d|[A-Z][a-z]+")  # a number or a capitalized word


@pytest.mark.asyncio
@pytest.mark.parametrize("video_input", TEST_VIDEO_INPUTS, ids=lambda v: v.video_category)
async def test_analyzer_produces_valid_brief(video_input):
    brief = await analyzer.run(video_input)

    assert isinstance(brief, VideoBrief)
    assert brief.core_promise.strip() != ""
    assert 0.0 <= brief.emotional_potential <= 1.0
    assert len(brief.trigger_candidates) > 0
    assert all(t.startswith("T") for t in brief.trigger_candidates)

    if HAS_ENTITY_SIGNAL.search(video_input.video_transcript):
        assert len(brief.key_entities) > 0, (
            "Transcript clearly contains proper nouns/numbers but "
            "key_entities came back empty."
        )
