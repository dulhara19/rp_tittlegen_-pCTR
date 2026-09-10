"""Critic Agent (SOT §12.3) — gatekeeper and ranker.

Scores each Generator candidate on virality (pCTR), arousal (VADER), and
faithfulness (BERTScore + NLI), hard-rejects contradictions, and ranks the
rest by composite score (SOT §11.4).

Scoring is parallelized: each candidate's three scorers (pCTR, BERTScore,
NLI) run concurrently via asyncio.to_thread, and all 5 candidates are
scored concurrently via asyncio.gather -- 15 blocking calls fanned out
instead of run one at a time. This closes the Sprint 5 P95 latency gap
(measured ~29.5s/request end-to-end when Critic scored candidates
sequentially; per-candidate scoring alone was the bulk of that). sklearn
and torch release the GIL for most of their compute, so a thread pool
still buys real wall-clock concurrency for this CPU-bound work without the
cost of re-loading the pCTR/BERTScore/NLI models per process.
"""

import asyncio

from system.agents.schemas import CriticOutput, GeneratorOutput, ScoredTitle, TitleCandidate, VideoBrief
from system.pipeline.bertscore_scorer import bert_similarity
from system.pipeline.category_map import category_name_to_id
from system.pipeline.nli_scorer import classify_nli
from system.pipeline.pctr_scorer import score_title

# Initial weights per SOT §11.4 (to be tuned).
W_PCTR = 0.50
W_VADER = 0.25
W_BERT = 0.25


async def _score_candidate(
    video_brief: VideoBrief, category_id: int, candidate: TitleCandidate
) -> ScoredTitle:
    (pctr_score, vader_compound), bert_sim, nli_label = await asyncio.gather(
        asyncio.to_thread(score_title, candidate.title, category_id),
        asyncio.to_thread(bert_similarity, candidate.title, video_brief.core_promise),
        asyncio.to_thread(classify_nli, candidate.title, video_brief.core_promise),
    )

    is_valid = nli_label != "contradiction"
    nli_multiplier = 1.0 if is_valid else 0.0
    composite_score = (
        W_PCTR * pctr_score + W_VADER * abs(vader_compound) + W_BERT * bert_sim
    ) * nli_multiplier

    return ScoredTitle(
        title=candidate.title,
        trigger_used=candidate.trigger_used,
        pctr_score=pctr_score,
        vader_compound=vader_compound,
        bert_similarity=bert_sim,
        nli_label=nli_label,
        composite_score=composite_score,
        is_valid=is_valid,
    )


async def run(
    video_brief: VideoBrief, generator_output: GeneratorOutput, video_category: str
) -> CriticOutput:
    category_id = category_name_to_id(video_category)

    scored_candidates = await asyncio.gather(
        *[_score_candidate(video_brief, category_id, c) for c in generator_output.candidates]
    )

    rejection_log = [
        f"{c.title!r} rejected: NLI contradiction against core_promise ({video_brief.core_promise!r})"
        for c in scored_candidates
        if not c.is_valid
    ]

    valid_candidates = [c for c in scored_candidates if c.is_valid]
    top_title = (
        max(valid_candidates, key=lambda c: c.composite_score).title if valid_candidates else ""
    )

    return CriticOutput(
        scored_candidates=list(scored_candidates),
        top_title=top_title,
        rejection_log=rejection_log,
    )
