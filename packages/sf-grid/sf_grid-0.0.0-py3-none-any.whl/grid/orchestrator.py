from typing import List, Any, Dict, Tuple, Union, Optional
import os
import code
import pickle
from multiprocessing.connection import Listener, Client
from collections import defaultdict
from grid import logger
from grid.notebook import Notebook
from grid.model.model import ModelCollection
from grid.registry import registry
from grid.assistant.schema import Message


def get_registered_cls(register_type: str, register_name: str) -> Any:
    if register_type == "World":
        return registry.get_world(register_name)
    elif register_type == "Robot":
        return registry.get_robot(register_name)
    else:
        raise ValueError(f"Registration class {register_type} not recognized")


# todo: let channel send in the code block itself, and deal with multiple receive messages
# todo: make rerun in browser and check if it is already open
class Channel:
    """inter-process communication channel between grid and executor, listens to localhost:7000 by default"""

    def __init__(self, port: int = 7000) -> None:
        self._conn = None
        self.port = port

    def close(self):
        self._conn.close()


class ListenChannel(Channel):
    """A class that represents a channel for communication between the orchestrator and the notebook. Default listening port is 6000.

    Returns:
        _type_: _description_
    """

    def __init__(self, timeout: float = 2.0) -> None:
        super().__init__()
        self.listener = Listener(("localhost", self.port))
        self.timeout = timeout
        self._conn = None

    def accept(self):
        self._conn = self.listener.accept()
        logger.info("connection established between grid and airgen exec env")

    def receive(self) -> dict:
        msg = {}
        while self._conn.poll(self.timeout):
            # todo: deal with multiple messages
            msg = pickle.loads(self._conn.recv_bytes())
        return msg

    def close(self) -> None:
        self._conn.close()
        self.listener.close()


class SendChannel(Channel):
    def __init__(self) -> None:
        super().__init__()
        self._conn = Client(("localhost", self.port))
        self._channel = {}

    def add(self, obj_key: Union[str, int], obj_val: Any) -> None:
        self._channel[obj_key] = obj_val

    def send(self) -> str:
        self._conn.send_bytes(pickle.dumps(self._channel))
        self._channel = {}

    def close(self) -> None:
        self._conn.close()


class Orchestrator:
    def __init__(
        self,
        cfg,
    ) -> None:
        # setup grid package configuration (grid package dir, etc)
        from grid import GRIDConfig

        self._main_dir = os.path.abspath(cfg.main_dir)
        self._iconfig = cfg.iconfig
        self._dconfig = cfg.debug
        # update dir for model to load weights and configs
        GRIDConfig.set_main_dir(self._main_dir)
        self.notebook = Notebook(os.path.join(self._main_dir, cfg.notebook_path))

        self._robots = cfg.robots
        self._world = cfg.world
        self._models = cfg.models
        self._init_code_prompt = ""
        self._listen_channel = ListenChannel()
        self._api_prompt = defaultdict(list)

    @property
    def main_dir(self) -> str:
        return self._main_dir

    @property
    def iconfig(self) -> int:
        """configuration for user interactions

        Returns:
            int: _description_
        """
        return self._iconfig

    def __enter__(
        self,
    ) -> str:
        """Setup initial code block for notebook.

        Returns:
            str: initial code cell
        """

        # setup kernel for notebook execute
        self.notebook.start()

        # setup grid package configuration (grid package dir)
        self.grid_pre_init()

        # setup initial code block that import relevant modules and initialize variables (visiable to gpt)
        self.import_statements = []
        self.init_statements = []
        self.variables = {}
        for robot in self._robots:
            self.initialize_class(robot, "Robot")
        logger.info("Robot ready")
        self.initialize_class(self._world[0], "World")
        logger.info("World ready")

        # add code for modelcollection
        if len(self._models) > 0:
            self.import_statements.append(
                "from grid.model.model import ModelCollection"
            )
            self.init_statements.append(
                f"""modelcollection=ModelCollection([{','.join('"'+model_name+'"' for model_name in self._models)}])"""
            )
            self._api_prompt["Models"].append(ModelCollection(self._models).prompt())

        logger.info("Models ready")

        self.import_statements.append("import math, numpy")
        # todo: find a nicer way to get prompt for models, robot and world
        init_code = "\n".join(self.import_statements + self.init_statements)
        self._init_code_prompt = f"Here is the initialization code that has already been run - feel free to use these objects that are already defined.\n```python\n{init_code}\n```"

        # run the initial code block
        cells = [
            self.notebook.create_text_cell("### Initialization"),
            self.notebook.create_code_cell(init_code),
        ]
        self.notebook.add_cells(cells)
        output = self.execute_last_cell_of_notebook()
        assert (
            output["stderr"] == ""
        ), f"Error in the initialization code block: {output['stderr']}"
        return self

    def grid_pre_init(self):
        """pre-initialization of grid package that is done for code execution the notebook:
        setup grid package configuration (grid package dir, etc)
        setup channel for communication between grid and executor (send channel)
        """
        grid_setup_config_code = [
            "import os",
            "os.environ['TURN_ON_RERUN'] = '1'",
            "from grid import GRIDConfig",
            f"GRIDConfig.set_main_dir('{self._main_dir}')",
            "from grid.orchestrator import SendChannel",
            "sender_channel = SendChannel()",
        ]
        cells = [
            self.notebook.create_text_cell("### Grid Config (invisiable to gpt)"),
            self.notebook.create_code_cell("\n".join(grid_setup_config_code)),
        ]
        self.notebook.add_cells(cells)
        output = self.execute_last_cell_of_notebook(force_execute=True)
        assert (
            output["stderr"] == ""
        ), f"Error in the pre-init of grid: {output['stderr']}"
        self._listen_channel.accept()
        return

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # clean up kernel of notebook executor
        self.notebook.terminate()
        self._listen_channel.close()
        return

    def api_prompt(self, categories: List[str]) -> str:
        return "\n".join(
            ["\n".join(self._api_prompt[category]) for category in categories]
        )

    @property
    def init_code_prompt(self) -> str:
        """Given variables and models, setup initial code block for notebook that imports relavant
        modules and initialize variables. The initial code block is also executed in the notebook.

        Returns:
            str: initial code block that import modules and initialize variables
        """
        return self._init_code_prompt

    def initialize_class(self, obj_config, obj_type) -> None:
        obj_name = obj_config["name"]
        self.variables[obj_name] = {
            "var_name": obj_name,
            "cls": get_registered_cls(obj_type, obj_name),
        }
        self._api_prompt[obj_type].append(self.variables[obj_name]["cls"].prompt())
        if obj_type == "Robot":
            self.variables[obj_name]["cls_name"] = self.variables[obj_name][
                "cls"
            ].__name__
            self.variables[obj_name]["cls_path"] = self.variables[obj_name][
                "cls"
            ].__module__
            # World object is not initialized in the notebook
            self.import_statements.append(
                f"from {self.variables[obj_name]['cls_path']} import {self.variables[obj_name]['cls_name']}"
            )
            if "init_args" in obj_config:
                self.init_statements.append(
                    f"{obj_name} = {self.variables[obj_name]['cls_name']}({','.join(obj_config['init_args'])})"
                )
            else:
                self.init_statements.append(
                    f"{obj_name} = {self.variables[obj_name]['cls_name']}()"
                )

    def execute_last_cell_of_notebook(
        self, force_execute: bool = False
    ) -> Dict[str, str]:
        """execute the last code cell in notebook,

        Args:
            force_executue (bool, optional): force the last cell to be executed regardless of debugging flags. Defaults to True.

        Returns:
            Dict[str, str]: _description_
        """
        if (not force_execute) and self._dconfig.get("no_exec", False):
            return {"stdout": "", "stderr": ""}
        output = self.notebook.execute_last_cell()
        return output

    def compile_code(self, code_snippet: str) -> str:
        """Extract code from actor's response and compile it to check for syntax error.

        Args:
            actor_code (str): extracted code blocks from actor's response

        Returns:
            str: feedback
        """
        if code_snippet == "":
            return "No code received."
        # compile the code to check for syntax error
        err_msg = ""
        try:
            code.compile_command(code_snippet, symbol="exec")
        except (SyntaxError, OverflowError, ValueError) as error:
            err_msg = f"Code has a compile error at line: {error.lineno}\n{error.text}\n{error.msg}"
        return err_msg

    def eval(
        self,
        user_task: Dict[str, str],
        actor_code_msg: Message,
        critic_code_msg: Optional[Message],
    ) -> Tuple[Dict[str, str], str]:
        """Evaluate actor's code and return error message if there is any.

        Args:
            user_task (Dict[str, str]): task description {"user_command": str, "plan": str, "user_feedback": str, "critic_feedback": str}
            actor_code_msg (Message): actor's solution to task which should be in markdown format and contain code block
            critic_code_msg (Optional[Message]): critic's feedback on actor's code
        refs: https://nbconvert.readthedocs.io/en/latest/execute_api.html#executing-notebooks-using-the-python-api-interface

        Returns:
            Dict[str, str]:
                "stdout": stdout of the last cell
                "stderr": stderr of the last cell
                "channel": values for variables in watch list
        """
        code_in_actor_msg = actor_code_msg.code
        err_msg = self.compile_code(code_snippet=code_in_actor_msg)
        if err_msg != "":
            return {"stdout": "", "stderr": f"complie error: {err_msg}"}

        cells = [
            self.notebook.create_text_cell("### Task:\n" + user_task["user_command"]),
            self.notebook.create_text_cell("#### Plan:\n" + user_task["plan"]),
            self.notebook.create_code_cell(code_in_actor_msg),
        ]
        # refactor to make a unified interface and treatment about input/output of execution
        self.notebook.add_cells(cells)
        output = self.execute_last_cell_of_notebook()

        # a separate cell to received data from code executor
        # todo: handle this piece of code to gpt
        actor_watch_list = actor_code_msg.json["watch_list"]
        critic_watch_list = (
            critic_code_msg.json["watch_list"] if critic_code_msg else []
        )
        watch_list = list(set(actor_watch_list) | set(critic_watch_list))
        state_cell = [
            self.notebook.create_code_cell(
                "\n".join(
                    [
                        f"for i,var in enumerate({watch_list}):",
                        "   var_value = globals().get(var, 'variable does not exist in the global scope')",
                        "   sender_channel.add(var, var_value)",
                        "sender_channel.send()",
                    ]
                )
            ),
        ]
        self.notebook.add_cells(state_cell)
        _ = self.execute_last_cell_of_notebook()
        # todo implement get values for variables in watch list
        received_values_for_watch_list = self._listen_channel.receive()
        output_channel = {}
        for var in watch_list:
            output_channel[var] = received_values_for_watch_list.get(
                var, f"value of variable {var} unavailable"
            )
        output["channel"] = output_channel
        return output
