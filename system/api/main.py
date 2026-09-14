"""FastAPI backend (SOT §14.1; PLAN §5.1) — the Facade layer over the
Analyzer -> Generator -> Critic pipeline.
"""

import re
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from system.agents.schemas import CriticOutput, GeneratorOutput, VideoBrief, VideoInput
from system.pipeline.config import LLM_MODEL
from system.pipeline.graph import run_pipeline
from system.pipeline.pctr_scorer import MODEL_NAME as PCTR_MODEL_NAME

app = FastAPI(title="AI-Powered YouTube Title Optimizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server (system/frontend)
    allow_methods=["*"],
    allow_headers=["*"],
)

MIN_TRANSCRIPT_WORDS = 50
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


def _sanitize(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", _HTML_TAG_RE.sub(" ", text)).strip()


class GenerateTitlesRequest(BaseModel):
    video_transcript: str
    video_description: Optional[str] = None
    video_category: str
    channel_stats: Optional[dict] = None

    @field_validator("video_transcript")
    @classmethod
    def _validate_transcript(cls, v: str) -> str:
        cleaned = _sanitize(v)
        word_count = len(cleaned.split())
        if word_count < MIN_TRANSCRIPT_WORDS:
            raise ValueError(
                f"video_transcript must have at least {MIN_TRANSCRIPT_WORDS} words "
                f"(got {word_count}) — insufficient signal for the Analyzer"
            )
        return cleaned

    @field_validator("video_description")
    @classmethod
    def _sanitize_description(cls, v: Optional[str]) -> Optional[str]:
        return _sanitize(v) if v else v

    @field_validator("video_category")
    @classmethod
    def _validate_category(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("video_category must not be empty")
        return cleaned


class GenerateTitlesResponse(BaseModel):
    video_brief: VideoBrief
    generator_output: GeneratorOutput
    critic_output: CriticOutput


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model_versions": {"llm": LLM_MODEL, "pctr_model": PCTR_MODEL_NAME},
    }


@app.post("/generate-titles", response_model=GenerateTitlesResponse)
async def generate_titles(request: GenerateTitlesRequest):
    video_input = VideoInput(
        video_transcript=request.video_transcript,
        video_description=request.video_description,
        video_category=request.video_category,
        channel_stats=request.channel_stats,
    )

    result = await run_pipeline(video_input)

    if result.get("error"):
        raise HTTPException(status_code=502, detail=result["error"])

    return GenerateTitlesResponse(
        video_brief=result["video_brief"],
        generator_output=result["generator_output"],
        critic_output=result["critic_output"],
    )
