"""LangGraph state machine (SOT §14.2; PLAN §5.3):
START -> Analyzer -> Generator -> Critic -> END.

Each node receives only the state slice it needs from the shared state dict
-- Generator and Critic never see video_input.video_transcript directly,
matching the anti-hallucination boundary established in Sprint 2/3.

Critic's scoring (pCTR/BERTScore/NLI) is CPU-bound, blocking work; it's
async internally (system/agents/critic.py fans each candidate's 3 scorers
and all 5 candidates out across a thread pool via asyncio.to_thread /
gather), so the critic node here just awaits it directly rather than
wrapping the whole call in its own to_thread. A true ProcessPoolExecutor
(as PLAN §5.2 originally specified) would need to re-load the
pCTR/BERTScore/NLI models in every worker process — expensive and, for the
torch/transformers models, awkward to pickle across process boundaries on
Windows. sklearn/torch inference release the GIL for most of their work,
so a thread pool still buys real concurrency without that cost; documented
deviation, same pattern as prior sprints' pragmatic substitutions.
"""

from typing import Optional, TypedDict

from langgraph.graph import END, StateGraph

from system.agents import analyzer, critic, generator
from system.agents.schemas import CriticOutput, GeneratorOutput, VideoBrief, VideoInput


class PipelineState(TypedDict, total=False):
    video_input: VideoInput
    video_brief: VideoBrief
    generator_output: GeneratorOutput
    critic_output: CriticOutput
    error: Optional[str]


async def _analyzer_node(state: PipelineState) -> dict:
    try:
        brief = await analyzer.run(state["video_input"])
        return {"video_brief": brief}
    except Exception as exc:
        return {"error": f"Analyzer failed: {exc}"}


async def _generator_node(state: PipelineState) -> dict:
    if state.get("error"):
        return {}
    try:
        output = await generator.run(state["video_brief"], state["video_input"].video_category)
        return {"generator_output": output}
    except Exception as exc:
        return {"error": f"Generator failed: {exc}"}


async def _critic_node(state: PipelineState) -> dict:
    if state.get("error"):
        return {}
    try:
        output = await critic.run(
            state["video_brief"],
            state["generator_output"],
            state["video_input"].video_category,
        )
        return {"critic_output": output}
    except Exception as exc:
        return {"error": f"Critic failed: {exc}"}


def build_graph():
    graph = StateGraph(PipelineState)
    graph.add_node("analyzer", _analyzer_node)
    graph.add_node("generator", _generator_node)
    graph.add_node("critic", _critic_node)
    graph.set_entry_point("analyzer")
    graph.add_edge("analyzer", "generator")
    graph.add_edge("generator", "critic")
    graph.add_edge("critic", END)
    return graph.compile()


_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


async def run_pipeline(video_input: VideoInput) -> PipelineState:
    graph = get_graph()
    return await graph.ainvoke({"video_input": video_input})
