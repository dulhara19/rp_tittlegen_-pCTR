"""Single seam for LLM provider selection (SOT §14.3).

Every agent calls get_chat_model() instead of instantiating ChatOpenAI
directly. Provider is chosen via LLM_BASE_URL / LLM_API_KEY / LLM_MODEL in
system/.env (defaults to OpenAI gpt-4o).
"""

from langchain_openai import ChatOpenAI

from system.pipeline.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL


class _OpenAICompatChat(ChatOpenAI):
    """For OpenAI-compatible providers (DeepSeek, Ollama) that lack the
    json_schema response format: default structured output to tool calling."""

    def with_structured_output(self, schema, *, method="function_calling", **kwargs):
        return super().with_structured_output(schema, method=method, **kwargs)


def get_chat_model(temperature: float = 0.7) -> ChatOpenAI:
    if LLM_BASE_URL:
        return _OpenAICompatChat(
            model=LLM_MODEL, api_key=LLM_API_KEY, base_url=LLM_BASE_URL, temperature=temperature
        )
    return ChatOpenAI(model=LLM_MODEL, api_key=LLM_API_KEY, temperature=temperature)
