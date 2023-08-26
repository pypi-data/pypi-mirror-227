from typing import Dict, Any, Tuple, List, Optional
import os
import openai
import tiktoken
import logging
from . import LLM


def openai_setup():
    openai.api_key = os.environ["OPENAI_API_KEY"]
    openai.util.logger.setLevel(logging.WARNING)


# update this table using: https://platform.openai.com/docs/models/gpt-4
CONTEXT_LENGTH = {
    "gpt-4": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0613": 32768,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
}


# ref: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        # print(
        #     "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        # )
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


class GPT(LLM):
    def __init__(self, model: str, temperature: float = 1.0) -> None:
        openai_setup()
        self.model = model
        self.temperature = temperature
        self._context_length = CONTEXT_LENGTH[model]
        self._enc = tiktoken.encoding_for_model(self.model)

    @property
    def context_length(self) -> int:
        return self._context_length

    @property
    def is_local(self):
        return False

    def tokenize(self, text: str) -> str:
        return self._enc.encode(text)

    def num_tokens_in_messages(self, messages: List[Dict[str, str]]) -> int:
        """Return the number of tokens used by a list of messages.
        There might be an slight mismatch for model=='gpt-4' since it updates over time
        """
        return num_tokens_from_messages(messages, model=self.model)

    def chatCompletion(
        self, messages, max_tokens: Optional[int] = None
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """returns a single message for a single conversation

        Args:
            messages (List[Dict[str, str]]): a list of messages where each message is a dict {"role":..., "content":...}
            max_tokens (int, optional): max number of tokens to generate. Defaults to None.
        Returns:
            Dict[str, str]: api response, dict {"message":..., "finish_reason":...}
        """
        if max_tokens is None:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
        else:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=max_tokens,
            )
        metadata = response["usage"]
        return response["choices"][0], metadata

    async def aChatCompletion(self, messages) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Async version of chatCompletion

        Args:
            messages (_type_): a list of messages where each message is a dict {"role":..., "content":...}
            temperature (float, optional): _description_. Defaults to 1.0.

        Returns:
            Dict[str, str]: api response, dict {"message":..., "finish_reason":...}
            Dict[str, Any]: meta data of response
        """
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        metadata = response["usage"]
        return response["choices"][0], metadata

    def bChatCompletion(self, conversations) -> List[tuple]:
        """batch inference for conversations

        Args:
            conversations (List[conversations]): a list of conversations

        Returns:
            List[messages, metadata]: a list of responses where api response, each of type dict {"message":..., "finish_reason":...}
        """
        responses = openai.Completion.create(
            model=self.model,
            messages=conversations,
            temperature=self.temperature,
        )
        return [
            (responses[i]["choices"][0], responses[i]["usage"])
            for i in range(len(responses))
        ]
