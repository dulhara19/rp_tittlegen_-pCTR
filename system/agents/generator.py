"""Generator Agent (SOT §12.2) — creative title factory.

Receives only the Analyzer's VideoBrief (plus video_category, which is
metadata, not raw transcript content, so passing it doesn't reopen the
anti-hallucination boundary) and produces 5 trigger-diverse title
candidates. Never sees the raw transcript.
"""

import re
from typing import List

from pydantic import BaseModel, Field

from system.agents.schemas import GeneratorOutput, TitleCandidate, VideoBrief
from system.pipeline.llm_client import get_chat_model
from system.pipeline.prompt_db import retrieve_examples

PERSONA = (
    "You are a viral YouTube title copywriter with 10+ years of experience "
    "optimizing CTR for top creators. You have deep expertise in "
    "psychological triggers, curiosity gaps, and emotional arousal "
    "engineering. Your goal is to write titles that are compelling, "
    "honest, and click-worthy."
)

_TRIGGER_NAMES = {
    "T1": "Curiosity Gap",
    "T2": "Loss Aversion / FOMO",
    "T3": "Social Proof / Authority",
    "T4": "Urgency / Scarcity",
    "T5": "Extreme / Superlative",
    "T6": "Personal Stakes / Vulnerability",
    "T7": "Number + Specificity",
}

MAX_CHARS = 100
TARGET_MIN, TARGET_MAX = 55, 70

_HAS_NUMBER = re.compile(r"\d")


class _RawCandidate(BaseModel):
    title: str
    trigger_used: str  # e.g. "T1 - Curiosity Gap"


class _RawGeneratorOutput(BaseModel):
    candidates: List[_RawCandidate] = Field(min_length=5, max_length=5)


def _build_prompt(video_brief: VideoBrief, examples: List[str]) -> str:
    triggers = video_brief.trigger_candidates or list(_TRIGGER_NAMES.keys())
    trigger_lines = "\n".join(f"  {t} - {_TRIGGER_NAMES.get(t, t)}" for t in triggers)
    example_lines = "\n".join(f"- {e}" for e in examples) or "(no examples retrieved)"
    has_numeric_entity = bool(video_brief.key_entities) and any(
        _HAS_NUMBER.search(e) for e in video_brief.key_entities
    )

    return f"""\
Video brief:
  core_promise: {video_brief.core_promise}
  key_entities: {", ".join(video_brief.key_entities) or "(none)"}
  emotional_potential: {video_brief.emotional_potential}
  authentically applicable triggers:
{trigger_lines}

Here are high-performing titles in this niche:
{example_lines}
Learn from their structure and psychological trigger patterns — do not copy them verbatim.

Work through these steps:
Step 1: Identify the core Information Gap or Conflict a viewer would want resolved, based only on the video brief above.
Step 2: Determine the strongest high-arousal emotional angle this content authentically supports.
Step 3: Draft one title for each of the authentically applicable triggers listed above.
Step 4: Include at least one loss-framing (T2) variant in the batch if the brief authentically supports a loss/mistake/avoidable-outcome framing; otherwise use the next-strongest applicable trigger instead — never fabricate a loss angle that isn't grounded in the brief.
{"Step 5: Include at least one variant built around the specific number(s) in key_entities." if has_numeric_entity else ""}
Step 6: Refine each title for mobile impact — target {TARGET_MIN}-{TARGET_MAX} characters, hard cap {MAX_CHARS}.
Step 7: Return exactly 5 titles, each tagged with the trigger it uses (format: "T1 - Curiosity Gap").

Constraints:
- Every title must be a truthful representation of core_promise — no claims beyond the video brief.
- No title may exceed {MAX_CHARS} characters.
- TRIGGER DIVERSITY IS MANDATORY: each of the 5 titles must use a different trigger from each other. Never submit two titles with the same trigger_used. If fewer than 5 triggers are authentically applicable, cover each applicable one at least once and use your best judgment for the rest — but do not repeat a trigger just because a title built around it worked well.
"""


def _to_candidate(raw: _RawCandidate) -> TitleCandidate:
    return TitleCandidate(
        title=raw.title,
        trigger_used=raw.trigger_used,
        char_count=len(raw.title),
        word_count=len(raw.title.split()),
    )


async def run(video_brief: VideoBrief, video_category: str) -> GeneratorOutput:
    examples = retrieve_examples(topic=video_brief.core_promise, category=video_category, k=5)

    llm = get_chat_model(temperature=0.9)
    structured_llm = llm.with_structured_output(_RawGeneratorOutput)

    messages = [
        {"role": "system", "content": PERSONA},
        {"role": "user", "content": _build_prompt(video_brief, examples)},
    ]
    raw_output: _RawGeneratorOutput = await structured_llm.ainvoke(messages)

    candidates = [_to_candidate(c) for c in raw_output.candidates]

    oversized = [c.title for c in candidates if c.char_count > MAX_CHARS]
    if oversized:
        raise ValueError(f"Generator produced title(s) over the {MAX_CHARS}-char hard cap: {oversized}")

    return GeneratorOutput(candidates=candidates)
