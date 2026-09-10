"""Shared Pydantic models for the agent pipeline (SOT §11.3).

One schema module for the whole pipeline — Analyzer, Generator, and Critic
all import from here rather than each agent redefining its own input/output
shapes.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class VideoInput(BaseModel):
    video_transcript: str
    video_description: Optional[str] = None
    video_category: str
    channel_stats: Optional[dict] = None  # {"subscribers": int, "avg_views": int}


class VideoBrief(BaseModel):
    core_promise: str
    key_entities: List[str]
    emotional_potential: float = Field(ge=0.0, le=1.0)
    trigger_candidates: List[str]  # e.g. ["T1", "T3", "T6"]


class TitleCandidate(BaseModel):
    title: str
    trigger_used: str  # e.g. "T1 - Curiosity Gap"
    char_count: int
    word_count: int


class GeneratorOutput(BaseModel):
    candidates: List[TitleCandidate] = Field(min_length=5, max_length=5)


class ScoredTitle(BaseModel):
    title: str
    trigger_used: str
    pctr_score: float = Field(ge=0.0, le=1.0)
    vader_compound: float = Field(ge=-1.0, le=1.0)
    bert_similarity: float
    nli_label: str  # "entailment" | "neutral" | "contradiction"
    composite_score: float
    is_valid: bool


class CriticOutput(BaseModel):
    scored_candidates: List[ScoredTitle]
    top_title: str
    rejection_log: List[str]
