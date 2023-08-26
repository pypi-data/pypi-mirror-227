from abc import ABC, abstractmethod
from typing import Dict, List


class LLM(ABC):
    @abstractmethod
    def is_local(self):
        raise NotImplementedError

    @abstractmethod
    def tokenize(self, text):
        raise NotImplementedError

    @abstractmethod
    def num_tokens_in_messages(self, message: List[Dict[str, str]]) -> int:
        raise NotImplementedError

    @abstractmethod
    def chatCompletion(self, messages):
        raise NotImplementedError

    @abstractmethod
    async def aChatCompletion(self, messages):
        raise NotImplementedError

    @abstractmethod
    def bChatCompletion(self, conversations):
        raise NotImplementedError


from .openai_gpt import GPT

llm_collections = {
    "gpt": GPT,
}

try:
    from .meta_llama import LLaMA
except ImportError:
    LLaMA = None

if LLaMA is not None:
    llm_collections["llama"] = LLaMA
__all__ = ["llm_collections"]
