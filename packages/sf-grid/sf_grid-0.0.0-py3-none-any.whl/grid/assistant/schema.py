import re
from typing import Any, Dict, List, Tuple, Type, Optional, Literal

import json
import copy
from grid import logger
from grid.assistant.llm import GPT


def conversation_token_stat(conversation: "Conversation") -> str:
    stat = f"{conversation._proxy}'s token usage:"
    stat += f"system prompt: {conversation._num_tokens_of_system_prompt}, messages: {conversation._num_tokens_of_msgs}, overall: {conversation._num_tokens_overall=}"
    return stat


def msgdict2str(msgdict: Dict[str, str]) -> str:
    """self-defined __str__ method for message dictionary {"role":..., "content":...}

    Args:
        msgdict (Dict[str, str]): message dictionary {"role":..., "content": $json_str}

    Returns:
        str: str representation for msgdict, mainly to be used in logging and printing
    """
    # todo: parse string inside json
    # todo: add ```python``` to code block
    return f"role:{msgdict['role']}\ncontent:\n{msgdict['content']}"


class Conversation:
    """Conversion history of chatbot."""

    def __init__(
        self,
        prompt_str: str,
        llm_context_length: int,
        logging_msgs: bool = True,
        proxy: str = "assistant",
    ) -> None:
        self._proxy = proxy
        self._msg_of_system_prompt = {"role": "system", "content": prompt_str}
        self._num_tokens_of_system_prompt: int = -1
        self._history = History()
        self._max_history_tokens: int = self._history._MAX_TOKENS_OF_SUMMARY
        self._messages = [copy.deepcopy(self._msg_of_system_prompt)]
        # keep track of number of tokens of each corresponding message
        self._num_tokens_of_msgs: List[int] = []
        self._num_tokens_overall: int = 0
        self._llm_context_length = llm_context_length

        # logging utilties
        self._logging_msgs = logging_msgs
        if logging_msgs:
            self._msgs_log = [self._msg_of_system_prompt]

    @property
    def logging_msgs(self) -> bool:
        return self._logging_msgs

    @property
    def messages(self) -> List[Dict[str, str]]:
        """Return message history.

        Returns:
            List[Dict[str, str]]: a list of messages including both user and llm's responses
        """
        return self._messages

    def set_prompt_metatdata(self, metadata: Dict[str, Any]) -> None:
        """Set metadata of prompt message. call this only after a llm chat completion with system prompt

        Args:
            metadata (Dict[str, Any]): metadata of prompt message
        """
        assert (
            self._num_tokens_of_system_prompt == -1
        ), "prompt metadata has been set already"
        self._num_tokens_of_system_prompt = metadata["prompt_tokens"]
        self._num_tokens_of_msgs.append(metadata["prompt_tokens"])
        self._num_tokens_overall = metadata["prompt_tokens"]

        assert (
            self._num_tokens_overall < self._llm_context_length
        ), f"prompt message exceeds max tokens of llm used by {self.__class__}"

        logger.debug("info after setting up prompt: %s", conversation_token_stat(self))

    def add_user_response(self, content: str) -> None:
        """Add to conversation response from user (any parties other than chatbot's own llm)"""
        self._messages.append({"role": "user", "content": content})
        if self._logging_msgs:
            self._msgs_log.append({"role": "user", "content": content})

    def add_llm_response(
        self, message: Dict[str, str], metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add to conversation response from llm, and metadata of the response and conversation

        Args:
            message (Dict[str, str]): message received from llm
            metadata (Optional[Dict[str, Any]], optional): _description_. Defaults to None.
        """
        logger.debug(f"adding new llm message to conversation: {message}")
        self._messages.append(message)
        if self._logging_msgs:
            self._msgs_log.append(message)

        if metadata is not None:
            # update token stats
            self._num_tokens_of_msgs.append(
                metadata["prompt_tokens"] - self._num_tokens_overall
            )  # tokens of last user response(s) between consecutive llm responses
            self._num_tokens_of_msgs.append(
                metadata["completion_tokens"]
            )  # number of tokens for this llm response
            self._num_tokens_overall = metadata["total_tokens"]
            logger.debug(
                "adding new llm message to conversation: %s",
                conversation_token_stat(self),
            )

            if self._num_tokens_overall > self._llm_context_length:
                logger.debug("cutting off messages of conversation")
                self.cutoff_msgs()
                logger.debug("info after cutoff: %s", conversation_token_stat(self))

    def cutoff_msgs(self) -> None:
        """cut off messages while keeping system prompt so that the resulting  number of tokens are within max_tokens

        #todo: cutoff at more semantically meaningful position

        Returns:
            None: _description_
        """
        num_tokens = (
            self._num_tokens_of_system_prompt + self._history._MAX_TOKENS_OF_SUMMARY
        )  # maximum number of tokens of the new system prompt
        cutoff_idx = (
            0  # index of the message, before which all messages will be cut off
        )
        for msg_idx in range(len(self._num_tokens_of_msgs) - 1, 0, -1):
            num_tokens += self._num_tokens_of_msgs[msg_idx]
            if num_tokens > self._llm_context_length:
                cutoff_idx = msg_idx + 1
                break
        self._history.dump(self._messages[1:cutoff_idx])
        sys_prompt = copy.deepcopy(self._msg_of_system_prompt)
        sys_prompt["content"] += f"/nHistory conversations:{self._history.summary}"
        self._messages = [sys_prompt] + self._messages[cutoff_idx:]
        if self._logging_msgs:
            self._msgs_log.append({"role": "history", "content": str(self._history)})
            self._msgs_log.append(
                {"role": "system_new", "content": sys_prompt["content"]}
            )
        # new system prompt tokens
        self._num_tokens_of_msgs = [
            self._num_tokens_of_system_prompt + 1 + self._history.num_tokens_of_summary
        ] + self._num_tokens_of_msgs[cutoff_idx:]
        # number of tokens of new system prompt + number of tokens of remaining messages
        self._num_tokens_overall = sum(self._num_tokens_of_msgs)
        return

    def __str__(self) -> str:
        """the str representation of conversation based on the logged messages!

        This function is expected to used in logging of conversation.

        Returns:
            str: _description_
        """
        return "\n".join([msgdict2str(m) for m in self._msgs_log])

    def log_multiple_llm_msgs(self, messages: List[Dict[str, Any]]) -> None:
        """Add to logs the response. This is only for logging purpose, not for actual conversation feed to llm."""
        if self._logging_msgs:
            for i, message in enumerate(messages):
                self._msgs_log.append(
                    {"role": message["role"] + f"_{i}", "content": message["content"]}
                )


class History:
    """a class for saving memory pieces"""

    # magic number
    _MAX_TOKENS_OF_SUMMARY = 200

    SYSTEM_PROMPT = "You are summarizing the history of a conversation. Each time, you are given a list of messages betwen user and assistent, and possibly a  brief summary of history earlier than that. Your task is to response a succint summary that shows the main gist of the conversation."

    def __init__(self) -> None:
        self._history = []
        self._summary: str = ""
        self._num_tokens_of_summary = 0
        self._llm4summary = GPT("gpt-4")  # hard coded gpt-4 for summary for now

    @property
    def num_tokens_of_summary(self) -> int:
        return self._num_tokens_of_summary

    def dump(self, msg_chunks: List[Dict[str, str]]) -> None:
        # invoke new summary of history so far
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"history:{self._summary}\nmost recent messages:\n"
                + "\n".join(
                    [f"role:{m['role']}\ncontent:{m['content']}" for m in msg_chunks]
                ),
            },
        ]
        (response, metadata) = self._llm4summary.chatCompletion(
            messages=messages, max_tokens=self._MAX_TOKENS_OF_SUMMARY
        )
        self._history += msg_chunks
        self._summary = response["message"]["content"]
        self._num_tokens_of_summary = metadata["completion_tokens"]

    def retrieve(self, query: str) -> List[Dict[str, str]]:
        """retrieve most relevant messages w.r.t. query from history

        Args:
            query (str): _description_

        Raises:
            NotImplementedError: _description_

        Returns:
            List[Dict[str, str]]: _description_
        """
        raise NotImplementedError

    def QA(self, query: str) -> str:
        """given a question, rerieve most relevant messages from histroy and ask llm to answer the question given retrieved messages

        Args:
            query (str): _description_

        Returns:
            str: _description_
        """
        raise NotImplementedError

    @property
    def summary(self) -> str:
        return self._summary

    def __str__(self) -> str:
        history_str = f"history contains the past {len(self._history)} messages:\nThe summary those messages:\n{self._summary}"
        return history_str


def extract_md_blocks(block_type: Literal["python", "json"], text: str) -> List[str]:
    """Extract markdown blocks from text string and concate them into a single raw string
    representation of code.

    Note:
        Although we specify in the prompt that a single python code block is expected, we still tend to get multiple code blocks in the response. This function is to extract all code blocks and concate them into a single string repr of code.
    """
    assert block_type in [
        "python",
        "json",
    ], f"supported block types: python, json, not {block_type}"
    blocks = re.findall(rf"```{block_type}(.*?)```", text, re.DOTALL)
    return blocks


def escape_chars_in_quotes(json_str: str) -> str:
    """ensure that the escape characters in those strings are properly formatted for JSON

    Args:
        s (str): _description_

    Returns:
        str: _description_
    """

    def replacer(match):
        # Replace \n with \\n in the matched string
        return match.group(0).encode("unicode_escape").decode()

    # Replace all instances of \n inside quotes
    json_str = re.sub(r'".*?"|\'.*?\'', replacer, json_str, flags=re.DOTALL)
    return json_str


def get_JSONdecode_err_msg(err: json.decoder.JSONDecodeError, json_str: str) -> str:
    def safe_index(i):
        return max(0, min(i, len(json_str) - 1))

    surrounding = (
        json_str[safe_index(err.pos - 15) : err.pos],
        json_str[err.pos],
        json_str[safe_index(err.pos + 1) : safe_index(err.pos + 15)],
    )
    surrounding = tuple(map(repr, surrounding))
    return f"JSON decode error: {err.msg}\nInvalid character {repr(json_str[err.pos])} at position: {err.pos}\nSurrounding content: {surrounding}"


class Message:
    """abstraction for processing message responded by llm.
    Note: it is not used in the Conversation class.

    Currenlt it only supports markdown format that contains [json string]? and [code block]? and [text]?
    """

    def __init__(
        self,
        message_dict: Dict[str, str],
        metadata: Dict[str, Any],
        json_format: Optional[Dict[str, Type]] = None,
    ) -> None:
        self._message = message_dict
        self.json_format = json_format
        self._json = {}
        self._code = ""
        self._num_tokens = metadata.get("completion_tokens", -1)
        self._metadata = metadata

    @property
    def num_tokens(self) -> int:
        "return -1 means meta data is not available"
        return self._num_tokens

    @property
    def content(self) -> str:
        return self._message["content"]

    @property
    def role(self) -> str:
        return self._message["role"]

    @property
    def raw_message(self) -> Dict[str, str]:
        """return message dict {"role":..., "content":...}"""
        return {k: v for k, v in self._message.items()}

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    @property
    def json(self) -> Dict[str, Any]:
        """return json object of the message, if not json format is provided, nor formatting failed, return empty dict.

        Returns:
            Dict[str, Any]: could be empty dict (use the return with caution)
        """
        assert (
            self._json != {}
        ), "json is not parsed yet, call to_json() first and check for its returned err_msg"
        return self._json

    @property
    def code(self) -> str:
        """return code block in the message, if no code block is found, return empty string.

        Returns:
            str: could be empty string (use the return with caution)
        """
        if self._code == "":
            code_blocks = extract_md_blocks("python", self.content)
            self._code = "\n".join(code_blocks)
        return self._code

    def to_json(self) -> str:
        """transform return message string (in json format) to dict with proper type. Always check if error message is empty before using the returned dict.

        Args:
            answer_format (Dict[str, Type]): _description_

        Returns:
            str: error message if not empty string
        """
        # todo: fix error on error mesg of parsing json not propogated back to gpt
        res = {}
        err_msg = ""
        try:
            # first find closing {} to extract json string
            json_blocks = extract_md_blocks("json", self.content)
            json_str = "{}"
            if len(json_blocks) == 0:
                err_msg = "no ```json``` block found"
            elif len(json_blocks) > 1:
                err_msg = "more than one ```json``` blocks found"
            else:
                json_str = json_blocks[0]
            # json_str = rsmove_extra_nls_for_json(json_str)
            json_str = escape_chars_in_quotes(json_str)  # json_str.
            res = json.loads(json_str)
        except json.decoder.JSONDecodeError as err:
            err_msg = get_JSONdecode_err_msg(err, json_str)
        if err_msg == "":
            # successfully decoded json, next check if needed fields are present with proper type
            for field, field_type in self.json_format.items():
                if res.get(field, "field does not exist") == "field does not exist":
                    err_msg = f"field {field} is missing from response"
                    break
                if field_type == str:
                    continue
                # convert to type
                try:
                    res[field] = field_type(res[field])
                except ValueError:
                    err_msg = f"field {field} cannot be converted in type: {field_type}"
                if err_msg != "":
                    break
        if err_msg == "":
            self._json = res
        return err_msg
