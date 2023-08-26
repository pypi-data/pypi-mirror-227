import os
import logging

GRID_MODULE_NAME = "grid"

# --- setup loggers for grid -------
logging_level = logging.INFO
logger = logging.getLogger(GRID_MODULE_NAME)
logger.setLevel(logging_level)  # INFO
# Create a handler. You can choose StreamHandler, FileHandler, etc.
log_handler = logging.StreamHandler()
log_handler.setLevel(logging_level)
# Create a formatter
log_formatter = logging.Formatter(
    "[%(name)s][%(asctime)s][%(levelname)s]-[%(filename)16s:%(lineno)4d] - %(message)s"
)
# Add the formatter to the handler
log_handler.setFormatter(log_formatter)
# Add the handler to the logger
logger.addHandler(log_handler)


# ---- setup grid configuration (mainly package dir) ------
class GRIDConfig:
    _main_dir = ""  # the dir that contains main.py and subdirectories like `./external`, './log` etc
    time_step = 0.01

    @classmethod
    def set_main_dir(cls, grid_dir: str) -> None:
        assert (
            cls._main_dir == ""
        ), f"GRIDConfig's main_dir is already set to {cls._main_dir}"
        cls._main_dir = grid_dir

    @classmethod
    def get_main_dir(cls) -> str:
        if cls._main_dir == "":
            cls._main_dir = os.path.dirname(os.path.abspath(__path__[0]))
            print(
                f"GRIDConfig's main_dir is null, setting it to the parent directory of grid package: {cls._main_dir}"
            )
        return cls._main_dir


# --- disable transformers's warning -------
try:
    import transformers

    transformers.logging.set_verbosity_error()
    logger.info("disabled transformers's warning")
except ImportError:
    logger.info("transformers not installed, skipping disabling transformers's warning")

# --- setup rerun (visualization tool) -----
import rerun as rr

# native viewer (depends on os)
# rr.init("grid", spawn=True)


# rerun viewer on browser
if os.environ.get("TRUN_ON_RERUN", "0") != "0":
    # setup the environment varible before importing grid to turn on rerun
    rr.init(GRID_MODULE_NAME)
    rr.serve()

# load .env file that contains OPENAI_API_KEY
from dotenv import load_dotenv

load_dotenv()
# suppress pydevd warning
os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

import grid.model
import grid.robot
import grid.world
