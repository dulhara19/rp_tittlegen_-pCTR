"""Automated Sprint 5 checks (PLAN_IMPLEMENTATION.md §5.5 exit criteria).

Uses Starlette's TestClient, which drives the ASGI app (including async
routes) synchronously, so no pytest-asyncio marker is needed here.

test_generate_titles_end_to_end makes real LLM + local-model calls across
all 10 fixtures (this is the Sprint 5 "10 real video transcripts" exit
criterion) — slow (~model already cached from Sprint 4, so LLM-latency
bound, not model-download bound) but intentionally exhaustive since this is
the one sprint whose exit criteria explicitly call for all 10.
"""

import time

import pytest
from fastapi.testclient import TestClient

from system.api.main import MIN_TRANSCRIPT_WORDS, app
from system.tests.fixtures import TEST_VIDEO_INPUTS

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "llm" in body["model_versions"]
    assert "pctr_model" in body["model_versions"]


def test_rejects_short_transcript():
    response = client.post(
        "/generate-titles",
        json={
            "video_transcript": "Too short.",
            "video_category": "Education",
        },
    )
    assert response.status_code == 422


def test_rejects_empty_transcript():
    response = client.post(
        "/generate-titles",
        json={"video_transcript": "", "video_category": "Education"},
    )
    assert response.status_code == 422


def test_accepts_unrecognized_category_via_fallback():
    """An 'invalid' category isn't rejected outright — category_map.py falls
    back to a default category_id (documented Sprint 2/4 behavior) rather
    than failing the request. This test locks in that behavior. Reuses a
    real fixture transcript (rather than nonsense text) so this counts
    toward validating the fallback path without adding a second distinct
    real-pipeline cost beyond what test_generate_titles_end_to_end already
    covers for a valid category.
    """
    video_input = TEST_VIDEO_INPUTS[0]
    response = client.post(
        "/generate-titles",
        json={
            "video_transcript": video_input.video_transcript,
            "video_category": "Not A Real Category",
        },
    )
    assert response.status_code != 422


def test_sanitize_strips_html_and_normalizes_whitespace():
    """_sanitize strips HTML markup (tags), not tag contents -- standard
    strip_tags semantics, matching PLAN §5.4's "strip HTML, normalize
    whitespace" requirement. It is not an XSS filter and doesn't need to be:
    this text is only ever fed to an LLM prompt and stored, never rendered
    as HTML in a browser.
    """
    from system.api.main import _sanitize

    assert _sanitize("<b>hello</b>  world") == "hello world"
    assert _sanitize("no tags here") == "no tags here"
    assert _sanitize("line1\n\n  line2\t\tline3") == "line1 line2 line3"


def test_pipeline_error_surfaces_as_502(monkeypatch):
    async def _boom(video_brief, video_category):
        raise RuntimeError("simulated LLM timeout")

    import system.pipeline.graph as graph_module

    monkeypatch.setattr(graph_module.generator, "run", _boom)
    graph_module._compiled_graph = None  # force rebuild so the monkeypatch takes effect
    try:
        transcript = " ".join(["word"] * (MIN_TRANSCRIPT_WORDS + 5))
        response = client.post(
            "/generate-titles",
            json={"video_transcript": transcript, "video_category": "Education"},
        )
        assert response.status_code == 502
        assert "simulated LLM timeout" in response.json()["detail"]
    finally:
        graph_module._compiled_graph = None


@pytest.mark.parametrize("video_input", TEST_VIDEO_INPUTS, ids=lambda v: v.video_category)
def test_generate_titles_end_to_end(video_input):
    payload = {
        "video_transcript": video_input.video_transcript,
        "video_description": video_input.video_description,
        "video_category": video_input.video_category,
        "channel_stats": video_input.channel_stats,
    }
    start = time.perf_counter()
    response = client.post("/generate-titles", json=payload)
    elapsed = time.perf_counter() - start

    assert response.status_code == 200, response.text
    body = response.json()["critic_output"]
    assert len(body["scored_candidates"]) == 5
    assert body["top_title"] != "" or all(
        c["nli_label"] == "contradiction" for c in body["scored_candidates"]
    )
    print(f"\n[{video_input.video_category}] {elapsed:.1f}s")
