from typing import Tuple

from grid.registry import registry
from grid.robot.robot import Robot
from grid.world.world import World


@registry.register_world(name="airgen_inspection")
class AirGenEnv(World):
    prompt_prefix = "sim"

    def __init__(self, robot: Robot) -> None:
        self._robot = robot
        self.objects_dict = {
            "turbine1": "BP_Wind_Turbines_C_1",
            "turbine2": "StaticMeshActor_2",
            "solarpanels": "StaticMeshActor_146",
            "crowd": "StaticMeshActor_6",
            "car": "StaticMeshActor_10",
            "tower1": "SM_Electric_trellis_179",
            "tower2": "SM_Electric_trellis_7",
            "tower3": "SM_Electric_trellis_8",
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
