"""Dynamic Prompt Database — vector retrieval of few-shot title examples
(SOT §13.1, §13.4; PLAN_IMPLEMENTATION.md §3.1).

`build()` is a one-time offline step (run via `python -m system.pipeline.prompt_db`)
that selects the top-N highest-virality titles *per category* from the
Sprint 1 dataset (a flat global top-200 was tried first but concentrated
almost entirely in a handful of viral-outlier categories — Music, Shorts,
movie trailers — starving niches like Education or Travel of same-category
examples and defeating the point of niche-specific retrieval, SOT §13.1),
labels each with a Hook Type from the same T1-T7 taxonomy the Analyzer
uses, embeds them, and persists a Chroma collection to system/data/prompt_db/.

`retrieve_examples()` is the runtime query path the Generator Agent calls.

Hook Type labeling is heuristic (keyword/regex rules), not the manual
annotation across 200 titles the plan originally called for — this mirrors
the Sprint 1 pattern of substituting a documented heuristic for a manual
labeling task under time constraints (see SOT §20 limitations).
"""

import os
import re
from pathlib import Path
from typing import List

import chromadb
import pandas as pd
from langchain_openai import OpenAIEmbeddings

from system.pipeline.category_map import category_name_to_id
from system.pipeline.config import OPENAI_API_KEY

BASE = Path(__file__).resolve().parent.parent
DATA_PATH = BASE / "data" / "processed" / "labeled_titles.csv"
PROMPT_DB_DIR = BASE / "data" / "prompt_db"
# EMBEDDING_PROVIDER=local uses sentence-transformers (no API key / credits);
# anything else uses OpenAI. Each provider gets its own Chroma collection since
# the vector dimensions differ.
EMBEDDING_PROVIDER = os.environ.get("EMBEDDING_PROVIDER", "openai").lower()
LOCAL_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "title_examples_local" if EMBEDDING_PROVIDER == "local" else "title_examples"
TOP_N_PER_CATEGORY = 15  # ~15 categories in category_map -> roughly 200 titles total
EMBEDDING_MODEL = "text-embedding-3-small"

# Ordered so the first matching pattern wins when a title matches more than
# one trigger's keywords — priority follows the analyzer's trigger taxonomy.
_HOOK_TYPE_RULES = [
    ("T7", re.compile(r"\d")),
    ("T4", re.compile(r"\b(now|today|before|last chance|deadline|hurry|breaking)\b", re.I)),
    ("T2", re.compile(r"\b(mistake|avoid|stop|wrong|never|warning|don't|regret)\b", re.I)),
    ("T3", re.compile(r"\b(everyone|million|expert|scientists?|study|according to|official)\b", re.I)),
    ("T5", re.compile(r"\b(best|worst|biggest|smallest|first|ever|most|craziest|insane|extreme)\b", re.I)),
    ("T6", re.compile(r"\b(i |my |we |me\b)", re.I)),
    ("T1", re.compile(r"\?|\b(secret|why|how|this is|you won't|revealed)\b", re.I)),
]
_DEFAULT_HOOK_TYPE = "T1"  # curiosity gap is the safest fallback for a bare headline


_local_model = None


def _embed(texts: List[str]) -> List[List[float]]:
    if EMBEDDING_PROVIDER == "local":
        global _local_model
        if _local_model is None:
            from sentence_transformers import SentenceTransformer

            _local_model = SentenceTransformer(LOCAL_EMBEDDING_MODEL)
        return _local_model.encode(texts, normalize_embeddings=True).tolist()
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY)
    return embeddings.embed_documents(texts)


def classify_hook_type(title: str) -> str:
    for trigger_code, pattern in _HOOK_TYPE_RULES:
        if pattern.search(title):
            return trigger_code
    return _DEFAULT_HOOK_TYPE


def build() -> None:
    df = pd.read_csv(DATA_PATH)
    top = (
        df.sort_values("virality_score", ascending=False)
        .groupby("category_id", group_keys=False)
        .head(TOP_N_PER_CATEGORY)
        .copy()
    )
    top["hook_type"] = top["title"].apply(classify_hook_type)

    vectors = _embed(top["title"].tolist())

    PROMPT_DB_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(PROMPT_DB_DIR))
    client.delete_collection(COLLECTION_NAME) if COLLECTION_NAME in [
        c.name for c in client.list_collections()
    ] else None
    collection = client.create_collection(COLLECTION_NAME)

    collection.add(
        ids=[str(i) for i in top["video_id"].astype(str) + "_" + top.index.astype(str)],
        embeddings=vectors,
        documents=top["title"].tolist(),
        metadatas=[
            {"category_id": int(cat), "hook_type": hook}
            for cat, hook in zip(top["category_id"], top["hook_type"])
        ],
    )
    print(f"Indexed {collection.count()} titles -> {PROMPT_DB_DIR}")


def retrieve_examples(topic: str, category: str, k: int = 5) -> List[str]:
    """Nearest-neighbor search for titles similar to `topic`, filtered to
    the given category when the category has enough matches; falls back to
    an unfiltered search otherwise so a sparse niche still returns examples.
    """
    query_vector = _embed([topic])[0]

    client = chromadb.PersistentClient(path=str(PROMPT_DB_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    category_id = category_name_to_id(category)
    result = collection.query(
        query_embeddings=[query_vector],
        n_results=k,
        where={"category_id": category_id},
    )
    documents = result["documents"][0] if result["documents"] else []

    if len(documents) < k:
        fallback = collection.query(query_embeddings=[query_vector], n_results=k)
        fallback_docs = fallback["documents"][0] if fallback["documents"] else []
        seen = set(documents)
        for doc in fallback_docs:
            if doc not in seen:
                documents.append(doc)
                seen.add(doc)
            if len(documents) >= k:
                break

    return documents[:k]


if __name__ == "__main__":
    build()
