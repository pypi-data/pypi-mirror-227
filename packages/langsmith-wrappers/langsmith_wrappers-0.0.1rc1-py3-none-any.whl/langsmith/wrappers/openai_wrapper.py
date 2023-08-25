from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

from langsmith.wrappers.base import ModuleWrapper

if TYPE_CHECKING:
    import openai

_LLM_PATHS = {
    "openai.Completion.create",
    "openai.ChatCompletion.create",
    "openai.ChatCompletion.acreate",
    "openai.Complete.create",
}


class OpenAIWrapper(ModuleWrapper):
    def __init__(self, module: Any, module_path: Sequence[str] | None = None):
        super().__init__(module, module_path)
        full_path = object.__getattribute__(self, "_lc_full_path")
        if ".".join(full_path) in _LLM_PATHS:
            object.__setattr__(self, "_run_type", "llm")


def __getattr__(name: str) -> Any:
    if name == "openai":
        try:
            import openai
        except ImportError:
            raise ImportError(
                "OpenAI SDK is not installed. "
                "Please install it with `pip install openai`."
            )

        return OpenAIWrapper(openai)
    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = [
    "openai",  # noqa: F822
]
