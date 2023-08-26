from typing import Optional, Dict, Any, List, Tuple
import os
import llama
from . import LLM

# todo: design goals, the same conversation and and message interfaces work for general llm classes


def setup_llama():
    """setup distributed inference of llama on a single machine"""
    os.environ["RANK"] = "0"
    os.environ["WORLD_SIZE"] = "1"
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = "29500"


def construct_llama_respoonse(message, finish_reason: str = "stop"):
    """construct llama response from message and finish_reason"""
    return {"message": message, "finish_reason": finish_reason}


class LLaMA(LLM):
    _static_model = None

    def __init__(
        self,
        ckpt_dir: str,
        temperature: float = 0.6,
        max_seq_len: int = 512,
        max_batch_size: int = 4,
    ):
        setup_llama()
        assert max_seq_len <= 4096, "llama only supports max_seq_len <= 4096"
        self.temperature = temperature
        self.max_seq_len = max_seq_len
        self.max_batch_size = max_batch_size
        tokenizer_path = os.path.join(
            os.path.dirname(llama.__path__[0]), "tokenizer.model"
        )
        # put model on gpu by default
        if LLaMA._static_model is None:
            LLaMA._static_model = llama.Llama.build(
                ckpt_dir=ckpt_dir,
                tokenizer_path=tokenizer_path,
                max_seq_len=max_seq_len,
                max_batch_size=max_batch_size,
            )
        self._enc = LLaMA._static_model.tokenizer
        # todo: given llama is bad at coding, let it handle reasoning only and let chatgpt-3.5 to handle coding

    @property
    def is_local(self):
        return True

    def tokenize(self, text: str) -> List[int]:
        # !placeholder, I don't know how to setup the last two boolean arguments in llama
        return self._enc.encode(text, True, False)

    def num_tokens_in_messages(self, messages: List[Dict[str, str]]) -> int:
        raise NotImplementedError

    def chatCompletion(
        self,
        messages: List["Message"],
        top_p: float = 0.9,
        max_gen_len: Optional[int] = None,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """single dialog completion

        Args:
            dialog (List["Message"]): a single dialog that is a list of messages, each message is a dict ["role": ..., "content": ...]
            top_p (float, optional): Defaults to 0.9.
            max_gen_len (Optional[int], optional): Defaults to None.

        Returns:
            Response: of type dict {"message":..., "finish_reason":...}
            Metadata: {"tokens used"}
        """
        results = LLaMA._static_model.chat_completion(
            [messages],  # type: ignore, llama2 accepts batch inference by default
            max_gen_len=max_gen_len,
            temperature=self.temperature,
            top_p=top_p,
        )
        return construct_llama_respoonse(results[0]["generation"]), {}

    def bChatCompletion(
        self,
        conversations: List["Conversation"],
        top_p: float = 0.9,
        max_gen_len: Optional[int] = None,
    ) -> List[Tuple[Dict[str, str], Dict[str, Any]]]:
        """Batch completion of dialogs

        Args:
            dialogs (List[Conversation]): batch of dialogs
            top_p (float, optional): Defaults to 0.9.
            max_gen_len (Optional[int], optional): Defaults to None.

        Returns:
            List[Response]: List of responses
        """
        results = LLaMA._static_model.chat_completion(
            conversations,  # type: ignore
            max_gen_len=max_gen_len,
            temperature=self.temperature,
            top_p=top_p,
        )
        return [
            (construct_llama_respoonse(result["generation"]), {}) for result in results
        ]

    async def aChatCompletion(
        self,
        messages: List["Message"],
        top_p: float = 0.9,
        max_gen_len: Optional[int] = None,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Async version of chatCompletion, mainly because current assistant.py that uses gpt's async version

        Args:
            dialog (List): A single dialog that is a list of messages, each message is a dict ["role": ..., "content": ...]
            top_p (float): Defaults to 0.9.
            max_gen_len (Optional[int]): Defaults to None.

        Returns:
            Response: ["role": "assistant", "content": ...]
            Metadata: {"tokens used"}
        """
        results = LLaMA._static_model.chat_completion(
            messages,  # type: ignore
            max_gen_len=max_gen_len,
            temperature=self.temperature,
            top_p=top_p,
        )
        return construct_llama_respoonse(results[0]["generation"]), {}


if __name__ == "__main__":
    ckpt_dir = "/home/shuhang/data/model_weights/llama-2-7b-chat"
    llama_model = LLaMA(ckpt_dir=ckpt_dir)

    from grid.assistant.schema import Conversation, Message

    prompt_path = "/home/shuhang/work/GRID/config/prompt/1m/airgen_actor.txt"
    prompt = open(prompt_path, "r").read()
    conv = Conversation(prompt_str=prompt)
    conv.add_user_response("fly to position (0, 0, -20)")

    resluts = llama_model.chatCompletion(conv.messages)
    print(resluts)
