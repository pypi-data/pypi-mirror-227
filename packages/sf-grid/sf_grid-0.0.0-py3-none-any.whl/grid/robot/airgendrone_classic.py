import os
from platform import uname
from typing import List, Tuple
import airgen
import numpy as np
from grid.registry import registry
from grid.robot.robot import Robot


@registry.register_robot(name="airgendrone_classic")
class AirGenDrone(Robot):
    prompt_prefix = ""

    def __init__(self) -> None:
        if (
            "linux" in uname().system.lower() and "microsoft" in uname().release.lower()
        ):  # In WSL2
            if "WSL_HOST_IP" in os.environ:
                HOST = os.environ["WSL_HOST_IP"]
                self.client = airgen.MultirotorClient(ip=HOST)
        else:
            self.client = airgen.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

    def takeoff(self) -> None:
        """Makes the drone take off."""
        self.client.takeoffAsync().join()

    def land(self) -> None:
        """Makes the drone land."""
        self.client.landAsync().join()

    def fly_to(self, point: Tuple[float, float, float], velocity: float) -> None:
        """Makes the drone fly to the point specified as a tuple of X, Y, Z coordinates with a
        specified velocity in m/s."""
        self.client.moveToPositionAsync(point[0], point[1], point[2], velocity).join()

    def fly_path(
        self, points: List[Tuple[float, float, float]], velocity: float
    ) -> None:
        """Makes the drone fly through a set of points specified as a list of tuple of X, Y, Z coordinates with a specified velocity in m/s"""
        airgen_points = []
        for point in points:
            airgen_points.append(airgen.Vector3r(point[0], point[1], point[2]))
        self.client.moveOnPathAsync(
            airgen_points,
            velocity,
            120,
            airgen.DrivetrainType.ForwardOnly,
            airgen.YawMode(False, 0),
            -1,
            1,
        ).join()

    def is_point_in_collision(self, point: Tuple[float, float, float]):
        """Returns a bool indicating whether the given point is in collision with any obstacles."""
        return self.client.isPointInCollision(airgen.Vector3r(point))

    def plan_and_fly_path(
        self,
        start: Tuple[float, float, float],
        goal: Tuple[float, float, float],
        velocity: float,
    ):
        """Plans a collision-free path between two points: start and goal specified as tuples of X,
        Y, Z coordinates, and then makes the drone fly through the planned safe path between those
        two points at the specified velocity in m/s."""
        trajectory = self.client.simPlanPath(
            airgen.Vector3r(start[0], start[1], start[2]),
            airgen.Vector3r(goal[0], goal[1], goal[2]),
            True,
            True,
        )

        if len(trajectory) > 1:
            waypoints = [(d["x_val"], d["y_val"], d["z_val"]) for d in trajectory]
            self.fly_path(waypoints, velocity)
        else:
            raise Exception("One of the points is invalid.")

    def get_robot_position(self) -> Tuple[float, float, float]:
        """Returns the current position of the drone in the global reference frame."""
        pose = self.client.simGetVehiclePose()
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]

    def get_yaw(self) -> float:
        """Returns the current yaw angle of the drone in degrees, in the global reference frame."""
        orientation = self.client.simGetVehiclePose().orientation
        yaw = airgen.to_eularian_angles(orientation)[2]
        return np.degrees(yaw)

    def set_yaw(self, yaw: float) -> None:
        """Sets the yaw angle of the drone to the specified value in degrees."""
        self.client.rotateToYawAsync(yaw, 5).join()

    def capture_image_front_camera(self):
        """Captures and an RGB image from the front camera of the drone and returns it as a numpy
        array."""
        responses = self.client.simGetImages(
            [airgen.ImageRequest(0, airgen.ImageType.Scene, False, False)]
        )
        response = responses[0]
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(response.height, response.width, 3)
        img_rgb = img_rgb[:, :, ::-1]
        return img_rgb

    def capture_image_bottom_camera(self):
        """Captures and an RGB image from the bottom camera of the drone and returns it as a numpy
        array."""
        responses = self.client.simGetImages(
            [airgen.ImageRequest(3, airgen.ImageType.Scene, False, False)]
        )
        response = responses[0]
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(response.height, response.width, 3)
        img_rgb = img_rgb[:, :, ::-1]
        return img_rgb
