from typing import List
import os
from grid.registry import BaseRegistry
from grid.utils.sys_utils import obj2prompt


class ModelRegistry(BaseRegistry):
    @classmethod
    def get_model(cls, name: str):
        return cls._get_impl("Model", name)

    @classmethod
    def register_model(cls, to_register=None, name=None, assert_type=None):
        return cls._register_impl("Model", to_register, name)


modelregistry = ModelRegistry()


def _try_register_external_models():
    from grid import GRIDConfig
    import importlib.util
    import sys

    # hardcoded package name for external models, ok for now
    package_name = "emodel"
    external_model_path = os.path.join(
        GRIDConfig.get_main_dir(),
        "external",
        package_name,
        "__init__.py",
    )
    spec = importlib.util.spec_from_file_location(package_name, external_model_path)
    # Create a new module based on the spec
    module = importlib.util.module_from_spec(spec)

    # Execute the module
    try:
        sys.modules["emodel"] = module
        spec.loader.exec_module(module)
    except Exception as err:
        print("load external model package failed", err)


def _try_register_models():
    try:
        from grid.model.perception import _try_register_perception
        from grid.model.navigation import _try_register_navigate

    except ImportError as err:
        print("register model failed", err)

    _try_register_external_models()


class Model:
    prompt_prefix = ""

    def __init__(self) -> None:
        pass

    def prompt(self) -> str:
        return obj2prompt(self)


class ModelCollection:
    prompt_prefix = ""

    def __init__(self, model_names: List[str]) -> None:
        """Initialize models specified by model_names."""
        _try_register_models()
        self._models = {
            model_name: modelregistry.get_model(model_name)()
            for model_name in model_names
        }
        self._prompt = []

    def getModel(self, model_name: str) -> Model:
        """Given model's name, return the model obeject.

        Args:
            model_name (str): name of the model

        Returns:
            Model: model object
        """
        return self._models[model_name]

    def prompt(self) -> str:
        self._prompt = []
        self._prompt.append(
            f"You have a collection of models.\n```python\n{obj2prompt(self)}\n```"
        )

        self._prompt.append("Here is a list of models in the collection:\n")
        for model_name in self._models:
            self._prompt.append(
                f"- Model name: {model_name}\nmodel:\n```python\n{self._models[model_name].prompt()}\n```\n"
            )
        return "\n".join(self._prompt)
