import collections
from typing import Any, Callable, DefaultDict, Dict, Optional, Type


class Singleton(type):
    """Meta class for Types
    Args:
        type (_type_): _description_
    Returns:
        _type_: _description_
    """

    _instances: Dict["Singleton", "Singleton"] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseRegistry(metaclass=Singleton):
    """registry
    Args:
        metaclass (Singleton, optional): _description_. Defaults to Singleton.
    Returns:
        _type_: _description_
    """

    mapping: DefaultDict[str, dict] = collections.defaultdict(dict)

    @classmethod
    def _register_impl(
        cls,
        _type: str,
        to_register: Optional[Any],
        name: Optional[str],
        assert_type: Optional[Type] = None,
    ) -> Callable:
        def wrap(to_register):
            if assert_type is not None:
                assert issubclass(to_register, assert_type), f"{to_register} must be a subclass of {assert_type}"
            register_name = to_register.__name__ if name is None else name

            cls.mapping[_type][register_name] = to_register
            return to_register

        if to_register is None:
            return wrap
        else:
            return wrap(to_register)

    @classmethod
    def _get_impl(cls, _type: str, name: str) -> Type:
        res = cls.mapping[_type].get(name, None)
        if res == None:
            raise ValueError(
                f"{_type} {name} not registered. Registered {_type}s are {[key for key in cls.mapping[_type]]}"
            )
        return res


class Registry(BaseRegistry):
    @classmethod
    def register_robot(cls, to_register=None, name=None, assert_type=None) -> Callable:
        return cls._register_impl("Robot", to_register, name)

    @classmethod
    def get_robot(cls, name):
        return cls._get_impl("Robot", name)

    @classmethod
    def register_world(cls, to_register=None, name=None, assert_type=None) -> Callable:
        return cls._register_impl("World", to_register, name)

    @classmethod
    def get_world(cls, name):
        return cls._get_impl("World", name)


registry = Registry()
