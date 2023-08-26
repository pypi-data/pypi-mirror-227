from grid.utils.sys_utils import cls2prompt


class Robot:
    def __init__(self) -> None:
        pass

    @classmethod
    def prompt(cls) -> str:
        _prompt = []
        _prompt.append(
            f"Here is a list of APIs you can use to interact with the robot:\n```python\n{cls2prompt(cls)}\n```\n Note that the simulator uses the NED coordinate system so the Z coordinate should be negative for upwards. The robot always starts on the ground."
        )
        return "\n".join(_prompt)
