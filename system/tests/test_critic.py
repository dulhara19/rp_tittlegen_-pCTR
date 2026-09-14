"""Automated Sprint 4 checks (PLAN_IMPLEMENTATION.md §4.7 exit criteria).

End-to-end pipeline test (Analyzer -> Generator -> Critic) plus a targeted
NLI-rejection test with a deliberately injected contradictory title.

Only 3 of the 10 fixtures are used for the end-to-end run (not all 10) —
each case here loads/runs facebook/bart-large-mnli and a BERTScore model
per candidate on top of 2 real LLM calls, which is materially slower than
Sprint 2/3's LLM-only tests. Requires OPENAI_API_KEY and a built prompt DB.
"""

import pytest

from system.agents import analyzer, critic, generator
from system.agents.schemas import CriticOutput, TitleCandidate, VideoBrief
from system.pipeline.nli_scorer import classify_nli
from system.tests.fixtures import TEST_VIDEO_INPUTS


@pytest.mark.asyncio
@pytest.mark.parametrize("video_input", TEST_VIDEO_INPUTS[:3], ids=lambda v: v.video_category)
async def test_critic_produces_valid_output(video_input):
    brief = await analyzer.run(video_input)
    generator_output = await generator.run(brief, video_input.video_category)
    output = await critic.run(brief, generator_output, video_input.video_category)

    assert isinstance(output, CriticOutput)
    assert len(output.scored_candidates) == 5

    for scored in output.scored_candidates:
        assert 0.0 <= scored.pctr_score <= 1.0
        assert -1.0 <= scored.vader_compound <= 1.0
        assert scored.nli_label in {"entailment", "neutral", "contradiction"}
        assert scored.is_valid == (scored.nli_label != "contradiction")

    scores = [s.composite_score for s in output.scored_candidates]
    assert len(set(scores)) > 1, "Composite scores show no differentiation across candidates"

    valid = [s for s in output.scored_candidates if s.is_valid]
    if valid:
        assert output.top_title == max(valid, key=lambda s: s.composite_score).title
    else:
        assert output.top_title == ""


def test_nli_hard_rejects_deliberate_contradiction():
    """Sprint 4 exit criterion: NLI must reject an injected deceptive title
    that directly contradicts the video brief's core promise.
    """
    brief = VideoBrief(
        core_promise="This budget laptop consistently failed every benchmark test we ran.",
        key_entities=["budget laptop", "benchmark test"],
        emotional_potential=0.4,
        trigger_candidates=["T2"],
    )
    deceptive_candidate = TitleCandidate(
        title="This Laptop CRUSHED Every Benchmark We Threw At It",
        trigger_used="T5 - Extreme / Superlative",
        char_count=47,
        word_count=8,
    )

    label = classify_nli(premise=deceptive_candidate.title, hypothesis=brief.core_promise)
    assert label == "contradiction", (
        f"Expected NLI to flag a directly opposite claim as a contradiction, got {label!r}"
    )
