import logging
import os
import readline

import hydra
import openai
from dotenv import load_dotenv
from omegaconf import DictConfig
from termcolor import colored
import grid
from grid.assistant import Actor, Critic
from grid.orchestrator import Orchestrator
from grid.session import Session

# todo: demo fire

# todo: wire the output between kernel and main program
# todo: check logs to see if conversations are complete


# todo: add chain of thought in prompt
# todo: planning is helpful, should avoid having users looking at the code
# todo: check free region?
# todo: put vqa in the loop
# todo: a cheating function called by command to escape the trap
# todo: curate test points to test moveonpath function (drifting)
# todo: drifting, and projecting to free space
# todo: need a way to test if two points are in the same node


# todo: clean mess resulted from refactoring utils


@hydra.main(version_base=None, config_path="../config", config_name="airgen_gpt_3m")
def main(cfg: DictConfig) -> None:
    """:q to quit interaction keyinterrupt to interrupt the code currently running.

    Args:
        cfg (DictConfig): _description_
    """
    with Orchestrator(cfg) as oc:
        with Critic(
            cfg.grid_dir,
            cfg.critic.llm,
            api_prompt=oc.api_prompt(["Robot", "World", "Models"]),
            init_code_prompt=oc.init_code_prompt,
            prompt_context_path=cfg.critic.prompt_context_path,
        ) as critic, Actor(
            cfg.grid_dir,
            cfg.actor.llm,
            api_prompt=oc.api_prompt(["Robot", "World", "Models"]),
            init_code_prompt=oc.init_code_prompt,
            prompt_context_path=cfg.actor.prompt_context_path,
        ) as actor:
            with Session([actor, critic]) as session:
                task = {"command": "", "feedback_msg": ""}

                task["command"] = session.get_user_input()
                while session.is_active:
                    session.actor_think_loop(task, oc)
                    task["command"] = session.get_user_input()


if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]
    openai.util.logger.setLevel(logging.WARNING)
    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=logging.WARNING,
    )
    # suppress pydevd warning
    os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"
    main()
