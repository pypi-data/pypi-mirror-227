from typing import Tuple

from grid.registry import registry
from grid.robot.robot import Robot
from grid.utils.sys_utils import cls2prompt
from grid.world.world import World


# todo: world should provide apis that are sufficent to evalute if the task is solved, and describe the situation if not
@registry.register_world(name="airgen_fire")
class AirGenEnv(World):
    prompt_prefix = "sim"

    def __init__(self, robot: Robot) -> None:
        self._robot = robot
        self.objects_dict = {
            "fire": "Fire_Grd_BP_00_0",
            "sky_waypoint": "Actor_0",
            "vantage_point_2": "Actor_5",
            "vantage_point_3": "Actor_4",
            "vantage_point_4": "Actor_3",
        }

    def simGetAgentPosition(self) -> Tuple[float, float, float]:
        """Return position of the drone in the environment.

        Returns:
            Tuple[float, float, float]: coordinates(x,y,z) of the agent
        """
        return self._robot.simGetDronePosition()

    def simGetObjectPosition(self, object_name: str) -> Tuple[float, float, float]:
        """Return position of an object in the environment given its name.

        Args:
            object_name (str): the name of the object

        Returns:
            Tuple[float, float, float]: coordinates(x,y,z) of the object
        """
        object_id = self.objects_dict.get(object_name, "")
        if object_id == "":
            raise ValueError("Object not in the environment")
        object_pose = self._robot.client.simGetObjectPose(object_id)
        return (
            object_pose.position.x_val,
            object_pose.position.y_val,
            object_pose.position.z_val,
        )
