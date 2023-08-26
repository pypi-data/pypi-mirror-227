from grid.utils.sys_utils import cls2prompt


class World:
    """Interface between llm and world."""

    def __init__(self) -> None:
        pass

    @classmethod
    def prompt(cls) -> str:
        _prompt = []
        _prompt.append(
            f"Here is a list of APIs you can use to interact with the world:\n```python\n{cls2prompt(cls)}\n```\n"
        )
        _prompt.append(
            f"The following objects exist in the world that you can access locations for: ['fire', 'vantage_point_2', 'vantage_point_3', 'sky_waypoint']"
        )
        return "\n".join(_prompt)
