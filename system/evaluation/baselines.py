"""Baseline title generation for the human-eval / LLM-judge comparisons
(SOT §19.3).

Baseline A (descriptive): SOT §19.3 specifies "ground truth from video" --
these are synthetic transcripts with no real underlying YouTube video, so
there is no real ground-truth title to pull from. Uses video_description
as a documented stand-in (it's already written in a plain, descriptive
register, which is what Baseline A is meant to represent).

Baseline B (zero-shot LLM): a single plain prompt to the same LLM (GPT-4o)
with none of the system's trigger engineering, few-shot retrieval, or CoT
-- the counterfactual "what if we just asked the LLM directly" baseline.
"""

from system.agents.schemas import VideoInput
from system.pipeline.llm_client import get_chat_model


def baseline_a_descriptive(video_input: VideoInput) -> str:
    return video_input.video_description or video_input.video_transcript[:70].strip()


async def baseline_b_zero_shot(video_input: VideoInput) -> str:
    llm = get_chat_model(temperature=0.7)
    prompt = (
        "Write a single YouTube video title for the video described below. "
        "Return only the title text, nothing else -- no quotes, no explanation.\n\n"
        f"Transcript: {video_input.video_transcript}"
    )
    response = await llm.ainvoke([{"role": "user", "content": prompt}])
    return response.content.strip().strip('"')
