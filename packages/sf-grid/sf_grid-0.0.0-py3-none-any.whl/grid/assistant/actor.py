from typing import Dict, Tuple, Type, Any, Optional
import os
import re
import datetime
import os

from termcolor import colored
from .assistant import Assistant
from .schema import Conversation, Message
from .llm import llm_collections
from grid import logger


class Actor(Assistant):
    """Actor assistant that receives task description and generate code."""

    PLAN_RESPONSE_FORMAT = {"plan": str, "question": str, "confidence": float}
    CODE_RESPONSE_FORMAT = {"watch_list": list}
    EVAL_EXEC_RESPONSE_FORMAT = {"task_completed": bool, "feedback": str, "retry": bool}

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(proxy="actor", **kwargs)

    def draft_plan(self, task: Dict[str, str]):
        user_feedback = (
            f"user's feedback on previous plan:\n{task['user_feedback']}\n"
            if task["user_feedback"] != ""
            else ""
        )
        critic_feedback = (
            f"{task['critic_feedback']}\n" if task["critic_feedback"] != "" else ""
        )
        self._conversation.add_user_response(
            content=f"task:\n{task['user_command']}\n{user_feedback}{critic_feedback}Complete plan for the task:"
        )
        llm_message = self.get_msg_from_llm(json_format=Actor.PLAN_RESPONSE_FORMAT)
        print(self.terminal_prompt)
        print("Plan:\n" + llm_message.json["plan"])
        print("Question:\n" + llm_message.json["question"])
        print("task complexity:\n" + str(llm_message.json["task_complexity"]))
        print("Confidence:\n" + str(llm_message.json["confidence"]))
        print("auto_run:\n" + str(llm_message.json["auto_run"]))
        print(colored("actor plan ends", "dark_grey"))
        self._conversation.add_llm_response(
            llm_message.raw_message, llm_message.metadata
        )
        return llm_message

    def write_code(self, task, critic_code_msg: Optional[Message]) -> Message:
        critic_code_feedback = (
            f"You last code was not executed because:\n{critic_code_msg.json['feedback']}\n"
            if critic_code_msg is not None
            else ""
        )
        self._conversation.add_user_response(
            content=f"task:\n{task['user_command']}\nProposed plan:\n{task['plan']}\n{critic_code_feedback}Write complete code for proposed plan code:"
        )

        llm_message = self.get_msg_from_llm(json_format=Actor.CODE_RESPONSE_FORMAT)
        self._conversation.add_llm_response(
            llm_message.raw_message, llm_message.metadata
        )
        return llm_message

    def eval_exec(
        self, task: dict, exec_info: dict, critic_exec_msg: Optional[Message] = None
    ) -> Message:
        """evaluate the execution of the code/plan.

        Args:
            task (dict): _description_
            exec_info (dict): _description_
            critic_exec_msg (Optional[Message], optional): _description_. Defaults to None.

        Returns:
            Message: actor's evaluate of the execution
        """
        critic_exec_feedback = (
            f"Feedback from third party:\n{critic_exec_msg.json['feedback']}\n"
            if critic_exec_msg
            else ""
        )
        self._conversation.add_user_response(
            content=f"Result of the execution:{exec_info}\n{critic_exec_feedback}Evaluate the execution for the proposed plan:"
        )

        llm_message = self.get_msg_from_llm(json_format=Actor.EVAL_EXEC_RESPONSE_FORMAT)
        self._conversation.add_llm_response(
            llm_message.raw_message, llm_message.metadata
        )
        return llm_message
