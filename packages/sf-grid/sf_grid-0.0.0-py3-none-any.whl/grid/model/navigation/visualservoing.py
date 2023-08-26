import math
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from grid.model.model import Model, modelregistry
from grid.utils.airgen_utils.airgen_geometry import imagecoord2direction


@modelregistry.register_model(name="nav-visualservoing")
class VisualServoing(Model):
    """Visual Servoing Model, control the motion of robot based on vision feedback."""

    def __init__(self) -> None:
        """initialize parameters for the visual servoing model"""
        super().__init__()
        self._gain = 0.1

    def moveDrone2Target(
        self,
        target_image_coord: Tuple[float, float],
        camera_param: Dict[str, Any],
    ) -> Tuple[float, np.ndarray]:
        """move the drone towards the target in the image captured by the camera

        Args:
            target_image_coord (Tuple[float, float]): pixel coordinate (in xy format) of the target in the image plane
            camera_param (Dict[str, Any]): parameters of the camera that captures the target

        Returns:
            Tuple[float, np.ndarray]:
                float: delta_yaw(degrees)
                np.ndarray: velocity vector for the drone to move towards the target

        Example:
            >>> vs = VisualServoing()
            >>> delta_yaw, velocity = vs.moveDrone2Target((100, 100), {"width": 640, "height": 480, "fov": 90, "camera_orientation": (0, 0, 0)})
            >>> drone.simSetYaw(drone.simGetYaw() + delta_yaw)
            >>> # move the drone towards target with velocity v for 10 seconds
            >>> drone.simMoveByVelocity(v, 10)
        """
        # rotate the yaw of robot so that camera face directly to the target
        delta_yaw = (
            (target_image_coord[0] - camera_param["width"] / 2)
            / camera_param["width"]
            * camera_param["fov"]
        )
        target_direction = imagecoord2direction(target_image_coord, camera_param)
        v = np.array(target_direction) * 5.0
        return delta_yaw, v
