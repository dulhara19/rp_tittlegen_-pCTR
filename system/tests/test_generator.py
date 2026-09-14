"""Automated Sprint 3 checks (PLAN_IMPLEMENTATION.md §3.5 exit criteria).

Runs the Analyzer then the Generator end-to-end against the 10 synthetic
transcripts and checks schema conformance + the length/count constraints.
Retrieval relevance (3.5's "verified manually for 10 test cases") is
inherently manual — see manual_check_generator.py.

Requires OPENAI_API_KEY (system/.env), a built prompt DB
(python -m system.pipeline.prompt_db), and makes real API calls.
"""

import pytest

from system.agents import analyzer, generator
from system.agents.schemas import GeneratorOutput
from system.tests.fixtures import TEST_VIDEO_INPUTS


@pytest.mark.asyncio
@pytest.mark.parametrize("video_input", TEST_VIDEO_INPUTS, ids=lambda v: v.video_category)
async def test_generator_produces_valid_output(video_input):
    brief = await analyzer.run(video_input)
    output = await generator.run(brief, video_input.video_category)

    assert isinstance(output, GeneratorOutput)
    assert len(output.candidates) == 5

    triggers_used = {c.trigger_used.split(" ")[0] for c in output.candidates}
    assert len(triggers_used) > 1, "All 5 candidates used the same trigger"

    for candidate in output.candidates:
        assert candidate.title.strip() != ""
        assert candidate.char_count <= 100
        assert candidate.char_count == len(candidate.title)
        assert candidate.word_count == len(candidate.title.split())
