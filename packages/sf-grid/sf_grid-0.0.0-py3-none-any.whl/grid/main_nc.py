import os
from typing import Tuple, Optional, Dict

# do not remove readline eventhough it is not explicitly used
import readline
import hydra
from omegaconf import DictConfig
from termcolor import colored
from grid import logger
from grid.assistant import Actor, Critic, NoOpCritic
from grid.orchestrator import Orchestrator

PROMPT = "GRID> "


def task_planning(
    oc: Orchestrator, actor: Actor, critic: Optional[Critic] = None
) -> Tuple[Dict[str, str], str]:
    """user inputs tasks and grid responds with a plan. User can keep providing feedback before approving the plan

    Usage:
        input natural language to interact with grid
        special commands:
                    :q to quit interaction
                    :a to approve the plan
                    :r to reset the task and restart interaction

    Args:
        oc (Orchestrator): _description_
        actor (Actor): _description_
        critic (Optional[Critic]): _description_

    Returns:
        Tuple[Dict[str, str], str]: task information, and status (:q, :a, or "")
    """
    # todo: add mechansim to skip approve and let actor take full control (consider question answering scenario)
    status = ""
    task = {"user_command": "", "user_feedback": "", "critic_feedback": "", "plan": ""}
    while True:
        # two phases: planning and execution
        user_input = input(PROMPT).strip()
        if user_input == ":q":
            # quit the whole program
            print(colored("Quitting...", "dark_grey"))
            status = ":q"
            break
        elif user_input == ":a":
            # approve
            if task["plan"] == "":
                print(colored("No plan to approve", "red"))
                continue
            else:
                status = ":a"
                break
        elif user_input == ":r":
            # reset
            task = {
                "user_command": "",
                "user_feedback": "",
                "critic_feedback": "",
                "plan": "",
            }
            # ignore number of trials so far
            continue
        else:
            # use input is either task command or feedback
            if task["user_command"] == "":
                task["user_command"] = user_input
            else:
                task["user_feedback"] = user_input

        actor_plan_msg = actor.draft_plan(task)
        task["plan"] = actor_plan_msg.json["plan"]
        if oc.iconfig.allow_auto_run and actor_plan_msg.json["auto_run"]:
            status = ":a"
            return task, status
        if critic is not None:
            critic_eval_msg = critic.eval_plan(task)
            if not critic_eval_msg.json["approve"]:
                print(critic_eval_msg["plan"], type(critic_eval_msg["plan"]))
                print(colored(critic_eval_msg["feedback"], "yellow"))
                task["critic_feedback"] = critic_eval_msg["feedback"]
    return task, status


def task_exec(
    oc: Orchestrator,
    actor: Actor,
    task: Dict[str, str],
    critic: Optional[Critic] = None,
) -> Tuple[int, str]:
    # actor output code for the plan
    # todo: actor and evalute the exec too,
    feedback_msg = None
    for _ in range(oc.iconfig.max_exec_trials):
        actor_code_msg = None
        critic_code_msg = None
        if critic is None:
            actor_code_msg = actor.write_code(task, None)
        else:
            for _ in range(oc.iconfig.max_code_trials):
                actor_code_msg = actor.write_code(task, critic_code_msg)
                critic_code_msg = critic.eval_code(task, actor_code_msg)
                if critic_code_msg.json["approve"]:
                    break

        # puts code to execution
        exec_info = oc.eval(
            task,
            actor_code_msg,
            critic_code_msg,
        )
        critic_exec_msg = None
        if critic:
            critic_exec_msg = critic.eval_exec(task, actor_code_msg, exec_info)
        # todo: implement this
        feedback_msg = actor.eval_exec(task, exec_info, critic_exec_msg)
        # evaluate the execution
        # critic should be complementary to actor's own evalution (not decisive)

        if feedback_msg.json["task_completed"]:
            break

    # todo: here can be an anchor point to semantic breakpoint
    return feedback_msg


@hydra.main(version_base=None, config_path="../config", config_name="airgen_gpt_nc")
def main(cfg: DictConfig) -> None:
    """:q to quit interaction keyinterrupt to interrupt the code currently running.

    Args:
        cfg (DictConfig): _description_
    """
    with Orchestrator(cfg) as oc:
        with Actor(
            main_dir=oc.main_dir,
            llm_config=cfg.actor.llm,
            api_prompt=oc.api_prompt(["Robot", "Models"]),
            init_code_prompt=oc.init_code_prompt,
            prompt_context_path=cfg.actor.prompt_path,
        ) as actor:
            critic_cls = Critic if cfg.get("critic", None) else NoOpCritic
            with critic_cls(
                main_dir=cfg.main_dir,
                llm_config=cfg.critic.llm if cfg.get("critic", None) else None,
                api_prompt=oc.api_prompt(["Robot", "World", "Models"]),
                init_code_prompt=oc.init_code_prompt,
                prompt_context_path=cfg.critic.prompt_path
                if cfg.get("critic", None)
                else "",
            ) as critic:
                while True:
                    task, status = task_planning(oc, actor, critic)
                    if status == ":q":
                        break
                    # user approved plan
                    print(colored("Executing...", "dark_grey"))
                    task_exec(oc, actor, task, critic)


if __name__ == "__main__":
    main()
