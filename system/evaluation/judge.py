"""LLM-as-a-Judge evaluation (SOT §19.4; PLAN §6.4).

A GPT-4o judge scores a title against the video's core_promise on
Curiosity, Urgency, Relevance (1-5), matching SOT §19.4's rubric and prompt
structure. Deterministic (temperature=0.0) since this is meant to be a
scoring instrument, not a creative task.
"""

from pydantic import BaseModel, Field

from system.pipeline.llm_client import get_chat_model

JUDGE_PERSONA = "You are an expert YouTube growth strategist."

PROMPT_TEMPLATE = """\
Given the video summary below, evaluate this title on three dimensions (1-5):
- Curiosity (Information Gap created)
- Urgency (time/loss pressure felt)
- Relevance (how well it matches the content)

Video Summary: {summary}
Title: {title}
"""


class JudgeScore(BaseModel):
    curiosity: int = Field(ge=1, le=5)
    urgency: int = Field(ge=1, le=5)
    relevance: int = Field(ge=1, le=5)
    overall: int = Field(ge=1, le=5)
    reasoning: str


async def judge_title(summary: str, title: str) -> JudgeScore:
    llm = get_chat_model(temperature=0.0)
    structured_llm = llm.with_structured_output(JudgeScore)
    messages = [
        {"role": "system", "content": JUDGE_PERSONA},
        {"role": "user", "content": PROMPT_TEMPLATE.format(summary=summary, title=title)},
    ]
    return await structured_llm.ainvoke(messages)
