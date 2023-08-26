import asyncio
import re
from typing import List, Tuple, Dict
from termcolor import colored
import nbformat as nbf
from jupyter_client import KernelManager
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from nbclient.util import ensure_async, run_sync

from grid.utils.sys_utils import makedir, removefile


class Notebook:
    def __init__(self, notebook_path):
        makedir(notebook_path)
        removefile(notebook_path)
        self._nb_path = notebook_path

        self._nb = nbf.v4.new_notebook()
        self._nbkm = KernelManager()
        self._nbexecutor = NotebookClient(self._nb, km=self._nbkm)
        self._nbkc = None

    def start(self):
        self._nbexecutor.start_new_kernel()
        self._nbkc = self._nbexecutor.start_new_kernel_client()

    def terminate(self):
        self._nbkc.shutdown()
        self._nbkm.cleanup_resources()
        self._nbkc.stop_channels()

        # save notebook
        with open(self._nb_path, "w", encoding="utf-8") as f:
            nbf.write(self._nb, f)

    def create_code_cell(self, content):
        return nbf.v4.new_code_cell(content)

    def create_text_cell(self, content):
        return nbf.v4.new_markdown_cell(content)

    def execute_last_cell(self) -> Dict[str, str]:
        """Execute the last cell in the notebook.

        Returns:
            Dict[str, str]: output and error message from execution
        """
        err_msg = ""
        assert self._nb.cells[-1].cell_type == "code", "last cell is not code cell"
        try:
            self._nbexecutor.execute_cell(
                self._nb.cells[-1],
                len(self._nb.cells) - 1,
            )
        except CellExecutionError as err:
            err_msg = process_cell_error(err.traceback)
        except KeyboardInterrupt:
            print("interrupted by keyboard")
            self._nbexecutor.km.interrupt_kernel()
            err_msg = ":interrupt"
            self._nbexecutor.km.restart_kernel()
        finally:
            # save executed notebook
            nbf.write(self._nb, self._nb_path)
        # get output of execution and print it to terminal console
        output_msg = []
        for output in self._nb.cells[-1]["outputs"]:
            if output["output_type"] == "stream" and output["name"] == "stdout":
                output_msg.append(output["text"])
            elif output["output_type"] == "execute_result":
                output_msg.append(output["data"]["text/plain"])

        return {"stdout": "\n".join(output_msg), "stderr": err_msg}

    def add_cells(self, cells: List[Tuple[str, str]]):
        """Add cells to the notebook.

        Args:
            section (List[str]): list of cells
        """

        self._nb["cells"].extend(cells)


def remove_ansi_codes(string):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", string)


def remove_empty_lines(s):
    return "\n".join(line for line in s.splitlines() if line.strip())


def process_cell_error(err_msg):
    """Process the output error message from notebook execution.

       - remove ansi color
       - remove code replication
       - remove empty lines

    Args:
        err_msg (_type_): _description_

    Returns:
        _type_: _description_
    """
    err_msg = remove_ansi_codes(err_msg)
    # keep only trackback
    idx = err_msg.find("Traceback")
    if idx != -1:
        err_msg = err_msg[idx:]
    return "An error occurred while executing the code:\n" + remove_empty_lines(err_msg)
