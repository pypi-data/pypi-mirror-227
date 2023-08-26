from typing import Dict, Tuple, Union
import os
import random
from termcolor import colored
import datetime
from .assistant import Assistant
from .schema import Conversation, Message
from .llm import llm_collections


class NoOpCritic:
    """NoOp critic context manager that does not do anything"""

    def __init__(self, **kwargs):
        pass

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class Critic(Assistant):
    """llm agent for evaluating the plan, code, and execution.
    The evaluation method is designed to functional and relatively independent from the history conversation
    """

    EVAL_PLAN_RESPONSE_FORMAT = {"approve": bool, "feedback": str}
    EVAL_CODE_RESPONSE_FORMAT = {
        "approve": bool,
        "feedback": str,
        "watch_list": list,  # list of string
    }
    EVAL_EXEC_RESPONSE_FORMAT = {"completion": float, "feedback": str}

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(
            proxy="critic",
            **kwargs,
        )

    def eval_plan(self, task: Dict[str, str]) -> Message:
        """evaluates the plan proposed by user. It does consider user_feedback

        Args:
            task (Dict[str, str]): user's task description, must contain key "user_command", and "plan"

        Returns:
            Message: plan evaluation message from critic
        """
        self._conversation.add_user_response(
            content=f"task:\n{task['user_command']}\nProposed Plan to solve the task:\n{task['plan']}\nEvaluate the proposed plan:"
        )

        llm_message = self.get_msg_from_llm(
            json_format=Critic.EVAL_PLAN_RESPONSE_FORMAT
        )

        self._conversation.add_llm_response(
            llm_message.raw_message, llm_message.metadata
        )
        return llm_message

    def eval_code(self, task: Dict[str, str], actor_code_msg: Message) -> Message:
        self._conversation.add_user_response(
            content=f"task:\n{task['user_command']}\nProposed plan:\n{task['plan']}\nProposed code:\n```python{actor_code_msg.code}```\nEvaluate the code for the proposed plan:"
        )

        llm_message = self.get_msg_from_llm(
            json_format=Critic.EVAL_CODE_RESPONSE_FORMAT
        )
        self._conversation.add_llm_response(
            llm_message.raw_message, llm_message.metadata
        )
        return llm_message

    def eval_exec(
        self,
        task: Dict[str, str],
        actor_code_msg: Message,
        exec_info: Dict[str, Union[str, dict]],
    ) -> Message:
        """Evaluate the execution of the code/plan.

        Args:
            task (Dict[str, str]): that contains "user_command", "plan", and "code"
            actor_code_msg (Message): actor code that contains "code"
            exec_info (Dict[str, Union[str, dict]]): contains "stdout", "stderr", "channel"

        Returns:
            Message: _description_
        """
        self._conversation.add_user_response(
            content=f"task:\n{task['user_command']}\nProposed plan:\n{task['plan']}\nExecution code:\n```python{actor_code_msg.code}```Result of the execution:{exec_info}\nEvaluate the execution for the proposed plan:"
        )

        llm_message = self.get_msg_from_llm(
            json_format=Critic.EVAL_EXEC_RESPONSE_FORMAT
        )
        self._conversation.add_llm_response(
            llm_message.raw_message, llm_message.metadata
        )
        return llm_message

    @property
    def prompt(self) -> str:
        return "\n".join(self._prompt)
