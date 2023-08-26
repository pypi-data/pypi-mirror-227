import os

# do not remove readline eventhough it is not explicitly used
import readline
import hydra
from omegaconf import DictConfig
from termcolor import colored
from grid import logger
from grid.assistant import Actor, Critic
from grid.orchestrator import Orchestrator

PROMPT = "GRID> "

# todo: fix duplicate rerun instances
# todo: let critic add code for channel
# todo: planning is helpful, should avoid having users looking at the code
# todo: a cheating function called by command to escape the trap

# todo: add fov to meta data for each type of images
# todo: channel and state tokenize
# todo: a channel handed out to gpt, let gpt decide what variables to include
# todo: inspection env with square buildings


@hydra.main(version_base=None, config_path="../config", config_name="airgen_gpt_1m")
def main(cfg: DictConfig) -> None:
    """:q to quit interaction keyinterrupt to interrupt the code currently running.

    Args:
        cfg (DictConfig): _description_
    """
    with Orchestrator(cfg) as oc:
        # todo: critic and actor may have different init_code (critic may have access to world)
        with Critic(
            oc.main_dir,
            cfg.critic.llm,
            api_prompt=oc.api_prompt(["Robot", "World", "Models"]),
            init_code_prompt=oc.init_code_prompt,
            prompt_context_path=cfg.critic.prompt_context_path,
        ) as critic, Actor(
            oc.main_dir,
            cfg.actor.llm,
            api_prompt=oc.api_prompt(["Robot", "Models"]),
            init_code_prompt=oc.init_code_prompt,
            prompt_context_path=cfg.actor.prompt_context_path,
        ) as actor:
            actor_response = ""
            critic_response = ""
            execute_output = {"output": "", "err_msg": ""}
            task = {
                "command": "",
                "feedback_msg": "",
                "state": "",
                "last_code_not_executed": False,
            }
            while True:
                if not cfg.auto_feedback_loop or task["feedback_msg"] == "":
                    task["command"] = input(PROMPT).strip()

                    if task["command"] == ":q":
                        print(colored("Quitting...", "dark_grey"))
                        break
                    elif task["command"] == ":cls":
                        os.system("clear")
                        continue

                for _ in range(cfg.max_feedback_trials):
                    actor_msg = actor.solve_task(task)
                    critic_code_eval_msg = critic.evaluate_solution(task, actor_msg)
                    if critic_code_eval_msg.json.get("approve", False):
                        break
                    task[
                        "last_code_not_executed"
                    ] = True  # gpt-4 constantly thinks previous code is executed
                    task["feedback_msg"] = critic_code_eval_msg.json.get("feedback", "")
                if cfg.auto_deploy != True:
                    print(colored("Deploy? [:d] or feedback", "dark_grey"))
                    deploying = input(PROMPT).strip()
                    if deploying == ":q":
                        print(colored("Quitting...", "dark_grey"))
                        break
                    elif deploying != ":d":
                        task["feedback_msg"] = deploying
                        task["last_code_not_executed"] = False
                        critic.receive_user_response(task, actor_msg)
                        continue

                print(colored("Executing...", "dark_grey"))
                execute_output, task["state"] = oc.eval(task["command"], actor_msg)
                if execute_output["err_msg"] == ":interrupt":
                    print(colored("Interrupted!", "dark_grey"))
                    task["feedback_msg"] = ""
                elif execute_output["err_msg"] != "":
                    print(execute_output["err_msg"])
                    # let critic know that the actor's solution is not correct
                    task["feedback_msg"] = execute_output["err_msg"]
                    # todo: remove redundancy in critic message
                    critic.receive_user_response(task, actor_msg)
                else:
                    # if there no error message, let critic evaluate the execution result
                    critic_exec_eval_msg = critic.evaluate_execution(
                        task, execute_output
                    )


if __name__ == "__main__":
    main()
