from typing import Dict, Type, Optional
import os
import datetime
import asyncio

from termcolor import colored
from grid import logger
from grid.utils.sys_utils import makedir
from .schema import Conversation, Message

from .llm import llm_collections


class Assistant:
    MAXIMUM_TRIALS = 5  # maximum number of trials to get a valid response (of the correct response) from llm

    def __init__(
        self,
        proxy: str,
        main_dir: str,
        llm_config: dict,
        api_prompt: str,
        init_code_prompt: str,
        prompt_context_path: str,
    ) -> None:
        self._proxy = proxy
        self.main_dir = main_dir
        self.llm_config = llm_config
        self.llm = self.build_llm(llm_config)
        self._api_prompt = api_prompt
        self._init_code_prompt = init_code_prompt
        self.prompt_context_path = os.path.join(self.main_dir, prompt_context_path)
        self.logfilepath = os.path.join(
            self.main_dir,
            f"log/{proxy}_log_{datetime.datetime.now().strftime('%Y_%m_%d')}.md",
        )

        self.terminal_prompt = colored(f"{proxy}: ", "red")

        # setup
        self.setup_prompt()

        self._conversation = Conversation(
            prompt_str=self.prompt,
            llm_context_length=self.llm.context_length,
            proxy=proxy,
        )
        self.set_prompt_metadata()

    def build_llm(self, llm_config):
        llm_class = llm_collections.get(llm_config["name"], None)
        assert llm_class is not None, f"{llm_config['name']} is not found in llm module"
        llm = llm_class(**llm_config["args"])
        return llm

    def set_prompt_metadata(self):
        """get number of tokens of the system prompt"""
        assert (
            len(self._conversation.messages) == 1
        ), "sending more than system prompt in `send_prompt_to_llm()`"
        num_tokens = self.llm.num_tokens_in_messages(self._conversation.messages)
        self._conversation.set_prompt_metatdata({"prompt_tokens": num_tokens})

    def __enter__(self) -> None:
        """When a session starts, write the time and model name to log file.

        Returns:
            _type_: _description_
        """
        self.open_log_file()
        return self

    def open_log_file(self):
        if self._conversation.logging_msgs:
            makedir(self.logfilepath)
            with open(self.logfilepath, "a+", encoding="utf-8") as f:
                f.write(
                    "\n"
                    + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    + ": session starts\n"
                    + f"llm: {self.llm_config}"
                )

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """When session ends, write the time to log file.

        Args:
            exc_type (_type_): _description_
            exc_value (_type_):self._messages = [self._prompt_msg]
        self._num_tokens_of_sys_prompt = -1
        self._num_overall_tokens = 0 _description_
            traceback (_type_): _description_
        """
        self.write_log_file_and_close()
        return

    def write_log_file_and_close(self):
        if self._conversation.logging_msgs:
            with open(self.logfilepath, "a", encoding="utf-8") as f:
                f.write(str(self._conversation) + "\n")
                f.write(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    + ": sesstion ends\n"
                )
        return

    def get_raw_msg_from_llm(self):
        raw_msg, metadata = self.llm.chatCompletion(
            messages=self._conversation.messages,
        )
        assert raw_msg["finish_reason"] == "stop", "LLM response is incomplete"
        return raw_msg["message"], metadata

    async def async_get_raw_msg_from_llm(self):
        # no need to add user response to log here, we only add it once in get_multiple_responses_from_llm
        raw_msg, metadata = await self.llm.aChatCompletion(
            messages=self._conversation.messages,
        )
        assert raw_msg["finish_reason"] == "stop", "LLM response is incomplete"
        return raw_msg["message"], metadata

    def get_msg_from_llm(self, json_format: Optional[Dict[str, Type]]):
        if json_format is None:
            # just return get messge without worrying about parsing json
            raw_message, metadata = self.get_raw_msg_from_llm()
            structured_message = Message(raw_message, metadata, None)
            return structured_message

        structured_message = None
        err_in_json_decode = ""
        for _ in range(Assistant.MAXIMUM_TRIALS):
            raw_message, metadata = self.get_raw_msg_from_llm()
            structured_message = Message(raw_message, metadata, json_format)
            err_in_json_decode = structured_message.to_json()
            if err_in_json_decode != "":
                logger.debug(f"err msg in getting json {err_in_json_decode}")
                self._conversation.add_llm_response(raw_message, metadata)
                self._conversation.add_user_response(content=err_in_json_decode)
            else:
                break
        if err_in_json_decode != "":
            logger.critical(
                f"{self.__class__} llm failed to respond with proper format after {self.MAXIMUM_TRIALS} trials: {err_in_json_decode}"
            )
            exit(1)
        return structured_message

    async def async_get_msg_from_llm(self, json_format: Dict[str, Type]):
        structured_message = None
        err_msg = ""
        for _ in range(Assistant.MAXIMUM_TRIALS):
            raw_message, metadata = await self.async_get_raw_msg_from_llm()
            structured_message = Message(raw_message, metadata, json_format)
            err_msg = structured_message.to_json()
            if err_msg != "":
                self._conversation.add_llm_response(raw_message, metadata)
                self._conversation.add_user_response(content=err_msg)
            else:
                break
        if structured_message.json is None:
            logger.info(
                f"{self.__class__} llm failed to respond with proper format after {self.MAXIMUM_TRIALS} trials: {err_msg}"
            )
            # when mutiple requests are made, we don't want to exit the program because of one failed request
        return structured_message

    async def async_get_msgs_from_llm(
        self, num_candidates, json_format: Dict[str, Type]
    ):
        """Send the complete conversation of chatbot to llm and get response from llm.

        Returns:
            dict: message from llm {"role": "assistant", "content": "..."}
        """

        results = await asyncio.gather(
            *[
                self.async_get_msg_from_llm(json_format=json_format)
                for _ in range(num_candidates)
            ]
        )
        self._conversation.log_multiple_llm_msgs(results)
        return results

    def get_multiple_msgs_from_llm(self, num_candidates, json_format):
        # use multiple async calls to (potentially?) save time
        return asyncio.run(self.async_get_msgs_from_llm(num_candidates, json_format))

    def setup_prompt(self):
        """Setup the prompt for the critic."""
        self._prompt = []
        with open(self.prompt_context_path) as f:
            self._prompt.append(f.read())
        self._prompt.append(self._api_prompt)
        from grid import __path__

        with open(os.path.join(__path__[0], "skill/skill.md"), "r") as f:
            self._prompt.append("Here is some skills the python code can use:")
            self._prompt.append(f.read())
        self._prompt.append(self._init_code_prompt)

    @property
    def prompt(self) -> str:
        return "\n".join(self._prompt)
