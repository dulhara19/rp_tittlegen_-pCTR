"""Analyzer Agent (SOT §12.1) — ground-truth extractor.

Reads raw video content and produces a VideoBrief. This is the primary
anti-hallucination boundary: everything downstream (Generator, Critic) only
ever sees this structured brief, never the raw transcript, so nothing the
Analyzer didn't ground in the transcript can leak into a generated title.
"""

from system.agents.schemas import VideoBrief, VideoInput
from system.pipeline.llm_client import get_chat_model

PERSONA = (
    "You are an analytical video content expert. You read raw video "
    "transcripts and extract only what is factually present — you do not "
    "embellish, infer beyond the text, or add creative interpretation."
)

INSTRUCTIONS = """\
Analyze the video content below and produce a structured brief by working \
through these steps:

Step 1: What does this video actually deliver to the viewer? Summarize this \
as one factual sentence — the core_promise.

Step 2: What real entities (proper nouns, numbers, names, stakes) are \
explicitly present in the transcript? List them as key_entities.

Step 3: What is the strongest truthful emotional angle this content \
authentically supports? Score this as emotional_potential, a float from 0 \
(no emotional angle) to 1 (maximum authentic emotional intensity).

Step 4: Which of the following psychological triggers authentically apply \
to this content, based only on what is actually in the transcript? List the \
applicable trigger codes as trigger_candidates.
  T1 - Curiosity Gap: an unresolved question/information gap
  T2 - Loss Aversion / FOMO: an avoidable mistake or loss being addressed
  T3 - Social Proof / Authority: expert input, scale, or crowd validation
  T4 - Urgency / Scarcity: time-bound or finite framing
  T5 - Extreme / Superlative: a genuinely extreme fact or outcome
  T6 - Personal Stakes / Vulnerability: first-person risk or loss
  T7 - Number + Specificity: exact, specific numbers or figures

CRITICAL ANTI-HALLUCINATION CONSTRAINT: Only include an entity in \
key_entities if it is verbatim or a clear, direct paraphrase of something \
stated in the transcript. If you are unsure whether something was actually \
stated, omit it. Do not invent names, numbers, or claims that are not in \
the transcript. The same applies to trigger_candidates: only select a \
trigger if the transcript authentically supports it — do not select a \
trigger just because it would make a punchier title.

Video transcript:
{video_transcript}

Video description (may be empty):
{video_description}

Video category: {video_category}
"""


async def run(video_input: VideoInput) -> VideoBrief:
    llm = get_chat_model(temperature=0.2)
    structured_llm = llm.with_structured_output(VideoBrief)

    prompt = INSTRUCTIONS.format(
        video_transcript=video_input.video_transcript,
        video_description=video_input.video_description or "(none provided)",
        video_category=video_input.video_category,
    )

    messages = [
        {"role": "system", "content": PERSONA},
        {"role": "user", "content": prompt},
    ]
    return await structured_llm.ainvoke(messages)
