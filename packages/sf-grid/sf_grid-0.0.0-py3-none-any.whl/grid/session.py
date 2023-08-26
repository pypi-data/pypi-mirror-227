import datetime
import os
import readline
from typing import Any, Dict, List

from termcolor import colored
from grid.orchestrator import Orchestrator

from grid.assistant.assistant import Assistant
from grid.utils import makedir


class Session:
    def __init__(self, llms: List[Assistant]) -> None:
        self.llms = llms
        self.prompt = "GRID> "
        self.active = True

        self.actor, self.critic = llms[0], llms[1]
        self.use_critic = True

        self.session_mode = "normal"

        self.normal_mode_message = "This session is in normal mode. You should write and execute code directly without the need for a plan or approval."
        self.mission_mode_message = "This session is in mission mode. You should output a plan and wait for approval before writing code."
        self.analysis_mode_message = "This session is an analysis mode. You should never write or execute any code."

    def __enter__(self) -> None:
        """When a session starts, write the time and model name to log file.

        Returns:
            _type_: _description_
        """

        # for llm in self.llms:
        #     makedir(llm.logfilepath)
        #     with open(llm.logfilepath, "a+", encoding="utf-8") as f:
        #         f.write(
        #             "\n"
        #             + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #             + ": session starts\n"
        #             + f"model: {llm.llm_config.model}"
        #         )
        # return self
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """When session ends, write the time to log file.

        Args:
            exc_type (_type_): _description_
            exc_value (_type_): _description_
            traceback (_type_): _description_
        """
        # for llm in self.llms:
        #     with open(llm.logfilepath, "a", encoding="utf-8") as f:
        #         f.write(str(llm.conversation) + "\n")
        #         f.write(
        #             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #             + ": sesstion ends\n"
        #         )
        # return
        return

    def get_user_input(self):
        user_command = input(self.prompt).strip()

        if user_command == ":cls":
            os.system("clear")
            user_command = input(self.prompt).strip()
        elif user_command == ":q":
            print(colored("Quitting...", "magenta"))
            self.active = False
        elif user_command == ":m":
            llm_input = {"command": "Enter mission mode", "feedback_msg": ""}
            response, code = self.actor.solve(llm_input)
            self.use_critic = True
            self.session_mode = "mission"
            user_command = input(self.prompt).strip()
        elif user_command == "~m":
            llm_input = {
                "command": "Exit mission mode and return to normal mode",
                "feedback_msg": "",
            }
            response, code = self.actor.solve(llm_input)
            self.use_critic = False
            self.session_mode = "normal"
            user_command = input(self.prompt).strip()

        return user_command

    @property
    def is_active(self):
        return self.active

    def evaluate_code(
        self,
        user_command: str,
        response: str,
        code_str: str,
        oc: Orchestrator,
        use_critic: bool,
    ):
        if use_critic:
            critic_response = self.critic.evaluate(user_command, code_str)

            if not critic_response.lower().startswith("approved"):
                return critic_response
        
        feedback = oc.eval(user_command, response, code_str)
        return feedback["err_msg"] if feedback["err_msg"] else feedback["output"]

    def actor_think_loop(self, llm_input: Dict, oc: Orchestrator):
        while True:
            print(colored("Thinking...", "dark_grey"))
            response, code_str = self.actor.solve(llm_input)

            if code_str:
                print(colored("Running code...", "light_blue"))
                llm_input["feedback_msg"] = self.evaluate_code(
                    llm_input["command"], response, code_str, oc, self.use_critic
                )
                if (
                    not llm_input["feedback_msg"]
                    or llm_input["feedback_msg"] == ":interrupt"
                ):
                    llm_input["feedback_msg"] = ""
                    break
            else:
                break
