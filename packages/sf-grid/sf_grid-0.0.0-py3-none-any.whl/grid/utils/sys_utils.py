import errno
import inspect
import logging
import os

from grid import logger as grid_logger

logger = grid_logger


def makedir(path: str):
    """Make directory if it does not exist.

    Args:
        path (str): path to directory
    """
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)


def removefile(path: str):
    """Remove the file at path if it exists.

    Args:
        path (str): path of the file to be removed
    """
    try:
        os.remove(path)
    except OSError as err:
        if err.errno != errno.ENOENT:
            raise
    return


def obj2prompt(obj) -> str:
    """Print string representation of obj to be used in prompt.

    Args:
        obj (Object): obj to be printed in prompt

    Returns:
        str: string respresention of object used in prompt
    """
    assert hasattr(obj, "prompt_prefix"), "obj must have prompt_prefix attribute"
    return cls2prompt(obj.__class__)


def cls2prompt(cls) -> str:
    """Print string representation of cls to be used in prompt.

    Args:
        cls (class): obj to be printed in prompt

    Returns:
        str: string respresention of object used in prompt
    """
    assert hasattr(cls, "prompt_prefix"), "obj must have prompt_prefix attribute"
    module_name = cls.__module__
    res = []
    res.append(f'class {cls.__name__}:\n\t"""{cls.__doc__}\n\t"""')
    for method_name in dir(cls):
        method = getattr(cls, method_name)
        if (
            callable(method)
            and hasattr(method, "__module__")
            and method.__module__ == module_name
        ):
            if (cls.prompt_prefix == "" and not method_name.startswith("prompt")) or (
                cls.prompt_prefix != "" and method_name.startswith(cls.prompt_prefix)
            ):
                signature = inspect.signature(method)
                docstring = method.__doc__
                if docstring is None:
                    logger.info(
                        "method: %s of class: %s has no docstring",
                        method_name,
                        cls.__name__,
                    )
                    docstring = ""
                res.append(
                    f'\tdef {method_name}{signature}:\n\t"""{docstring.rstrip()}\n\t"""\n'
                )
    return "\n".join(res)
