"""Implement drone in AirGen environment
    every angle in-out of this class is in degrees
"""
from typing import List, Dict, Any, Tuple
import math
import os
import json
import datetime
from time import perf_counter
import airgen
import numpy as np
from airgen.types import ImageType

from grid.registry import registry
from grid.robot.robot import Robot

from grid.utils.airgen_utils.airgen_sensor import responses2image, imagetype2request
from grid.utils.airgen_utils.airgen_generic import airgenClient

try:
    from grid.model.perception.vqa.gllava import GLLaVA
except ImportError:
    GLLaVA = None


# todo: hard code search radius and number of random points in each search, remove this in the future
MAX_SEARCH_RADIUS = 129.0

AIRGEN_IMAGE_TYPE = {
    "rgb": ImageType.Scene,
    "depth": ImageType.DepthPerspective,
    "segmentation": ImageType.Segmentation,
}


@registry.register_robot(name="airgendrone")
class AirGenDrone(Robot):
    prompt_prefix = "sim"

    def __init__(self, visual_assistant: bool = True) -> None:
        """Set up client and connect to airgen, and take off the drone.

        Args:
            visual_assistant (bool, optional): whether to use visual assistant. Defaults to True.
        """
        # keep a log for monitoring behvaiors of the drone
        from grid import GRIDConfig

        self.logfilepath = os.path.join(
            GRIDConfig.get_main_dir(),
            f"log/drone_log_{datetime.datetime.now().strftime('%Y_%m_%d')}.json",
        )
        # connect to airgen

        self.client: airgen.MultirotorClient = airgenClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

        self.camera_info_extra = {
            "front_center": self.getCameraInfo("front_center"),
            "bottom_center": self.getCameraInfo("bottom_center"),
        }
        self.last_free_pos = None
        self.simTakeoff()
        self._move_velocity = 1.0

        # models attached to drone
        if visual_assistant and GLLaVA is not None:
            self.rgbimage2text = GLLaVA()
        else:
            self.rgbimage2text = None

    @property
    def velocity(self) -> float:
        return self._move_velocity

    @velocity.setter
    def velocity(self, v: float) -> None:
        self._move_velocity = v

    def stateSummarizer(self) -> str:
        """return a string that summarizes the state of the drone

        Returns:
            str: a string that summarizes the state of the drone
        """
        if self.rgbimage2text is None:
            state = {
                "position": self.simGetDronePosition(),
                "distance (meters) above the ground": f"{float(np.mean(self.simGetImages('bottom_center', ['depth'])[0][0])):.2f}",
            }
        else:
            state = {
                "position": self.simGetDronePosition(),
                "what drone sees": self.rgbimage2text.run(
                    self.simGetImages("front_center", ["rgb"])[0][0],
                    "describe the image in detail",
                ),
                "distance (meters) above the ground": f"{float(np.mean(self.simGetImages('bottom_center', ['depth'])[0][0])):.2f}",
            }
        return json.dumps(state, indent=4)

    def getCameraInfo(self, camera_name: str):
        info = self.client.simGetCameraInfo(camera_name)
        return {"fov": info.fov}

    # def simMoveToPosition(self, position: Tuple[float, float, float]) -> None:
    #     """Move the drone to position: (x,y,z) respect to the world coordinate.

    #     Notes:
    #         The z-axis points downward, hence z decreases as the drone goes up. To GPT assistant: Don't flip the sign of position[2] or z-position when a complete position (x, y, z) is specified

    #     Args:
    #         Position (Tuple[float, float, float]): target position (x, y, z).
    #     """
    #     try:
    #         x, y, z = (float(position[i]) for i in range(3))
    #     except:
    #         raise ValueError(
    #             f"target position must be a tuple of three floats, but found x:{type(position[0])}, y:{type(position[1])}, z:{type(position[2])}"
    #         )

    #     self.client.moveToPositionAsync(x, y, z, 4).join()

    def simMoveByVelocity(
        self, velocity: Tuple[float, float, float], duration: int
    ) -> None:
        """Fly the drone with `velocity` (velocity vector is respect to world coordinates) for the
        specified `duration` of seconds.

        Args:
            velocity (Tuple[float, float, float]): three floats corresponding to the X, Y, Z components of velocity with respect to the world coordinate
            duration (int): number of seconds that the drone should be moving
        """
        # self.client.moveByVelocityAsync(
        #     velocity[0],
        #     velocity[1],
        #     velocity[2],
        #     duration,
        # ).join()
        current_position = self.simGetDronePosition()
        target_position = [
            current_position[i] + velocity[i] * duration
            for i in range(len(current_position))
        ]
        self.simMoveToPosition(target_position=target_position)
        self.client.moveByVelocityAsync(0, 0, 0, 0.1).join()
        # solutions:
        # 1. send zero velocity after duration
        # 2. have hover after move
        # 3. implement this with movetoposition()

    def simTakeoff(self) -> None:
        """Take off the drone."""
        self.client.takeoffAsync().join()
        # clear collision info
        self.client.simGetCollisionInfo()

    def simLand(self) -> None:
        """Land the drone."""
        self.client.landAsync().join()

    def simGetDronePosition(self) -> Tuple[float, float, float]:
        """Get the current position of the drone with respect to the world coordinate.

        Returns:
            Tuple[float, float, float]: drone's current position (x,y,z) with respect to the world coordinate
        """
        pose = self.client.simGetVehiclePose()
        return (pose.position.x_val, pose.position.y_val, pose.position.z_val)

    def hasCollided(self) -> bool:
        return self.client.simGetCollisionInfo().has_collided

    def simMoveToPosition(
        self,
        target_position: Tuple[float, float, float],
    ) -> None:
        """Move the drone to position: (x,y,z) respect to the world coordinate in collision-free manner. The z-axis of world coordinate points downward.
        Given that the target_position may be occupied  and imperfect control modules, error between actual position and target distance between 10 meters is acceptable.

        Args:
            target_position (Tuple[float, float, float]): target position (x, y, z).

        Example:
            >>> # move the drone to coordinate (20.0, 100.0, 30.0), no need to flip the sign of z when a complete position (x, y, z) is specified
            >>> drone.simMoveToPosition((20.0, 100.0, 30.0))
        """
        # todo: collect collision info during execution, and a mechanism to abort/reset
        try:
            x, y, z = (float(target_position[i]) for i in range(3))
            target_position = (x, y, z)
        except:
            raise ValueError(
                f"target position must be a tuple of three floats, but found x:{type(target_position[0])}, y:{type(target_position[1])}, z:{type(target_position[2])}"
            )
        # ! a hack way: start from last free position instead of current position becasue of drifting that causes
        # ! drone end up inside occupied space
        # assuming drone following a path given by simPlanPath() will not collide, so the end of planned path is free and a reasonable
        # coordinate to reset to
        # move to a previous free point
        # use teleport to avoid collision
        # can we update flynavi apis? it problem seems to be, whenever we are in a collision state, we can't move the drone

        # currently, if the goal position is not free, the drone will not move
        trajectory = []
        last_free_pos = (
            self.last_free_pos
            if self.last_free_pos is not None
            else self.simGetDronePosition()
        )
        distance = np.linalg.norm(
            [last_free_pos[i] - target_position[i] for i in range(len(last_free_pos))]
        )
        log = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "func_name": "simMoveToPosition",
            "args": {
                "last_free_position": last_free_pos,
                "target_position": target_position,
                "distance": distance,
            },
        }
        # print(f"{last_free_pos=}")
        search_radius = 0.0
        # find a non-empty path to the target position from the current position
        while search_radius < MAX_SEARCH_RADIUS:
            trajectory = self.client.simPlanPathToRandomizeGoal(
                start=airgen.Vector3r(
                    last_free_pos[0], last_free_pos[1], last_free_pos[2]
                ),
                goal=airgen.Vector3r(
                    target_position[0], target_position[1], target_position[2]
                ),
                search_radius=search_radius,
                num_trials=100,
                smooth_path=True,
                draw_path=False,
            )

            if trajectory is not None and len(trajectory) > 1:
                # print(f"found a trajectory with search radius {search_radius}")
                break
            else:
                search_radius = search_radius * 2 if search_radius > 0.5 else 1.0

        if trajectory is None or len(trajectory) < 2:
            print(
                f"no viable trajectory found between {last_free_pos} and {target_position} with search radius {search_radius}"
            )
            log["exec"] = {
                "target_position": target_position,
                "search_radius": search_radius,
                "result": "failed",
            }
            with open(self.logfilepath, "a+", encoding="utf-8") as f:
                # there is more work to do to make this json readable
                f.write(json.dumps(log, ensure_ascii=False, indent=4))
                f.write(",\n")
            return False
        # current_position = self.simGetDronePosition()
        # print(
        #    f"current position of drone that to be appended to trajectory: {current_position}"
        # )
        airgen_points = []

        for waypoint in trajectory:
            airgen_points.append(
                airgen.Vector3r(waypoint["x_val"], waypoint["y_val"], waypoint["z_val"])
            )
        start_time = perf_counter()
        self.client.moveOnPathAsync(airgen_points, self.velocity).join()
        self.client.moveByVelocityAsync(0, 0, 0, 0.1).join()
        # prevent the drone from drifting
        self.last_free_pos = (
            airgen_points[-1].x_val,
            airgen_points[-1].y_val,
            airgen_points[-1].z_val,
        )
        end_time = perf_counter()
        # log the behavior of this function for debugging
        log["exec"] = {
            "search_radius": search_radius,
            "seconds_elapsed": end_time - start_time,
            "trajectory": trajectory,
        }
        with open(self.logfilepath, "a+", encoding="utf-8") as f:
            # there is more work to do to make this json readable
            f.write(json.dumps(log, ensure_ascii=False, indent=4))
            f.write(",\n")
        return True

    def simSetYaw(self, yaw: float) -> None:
        """Set the yaw (in degrees) of the drone to the specified degrees. Yaw measures the
        rotation of the drone around the z-axis (downwards)

        Args:
            yaw (float): the target yaw (degrees!) for the drone, ranges from -180.0 to 180.0
        """
        self.client.rotateToYawAsync(float(yaw), 5).join()

    def simGetYaw(self) -> float:
        """Return the current yaw of the drone in degrees.

        Returns:
            float: yaw of the drone in degrees, ranges from -180.0 to 180.0
        """
        orientation_quat = self.client.simGetVehiclePose().orientation
        yaw = airgen.to_eularian_angles(orientation_quat)[2]
        return np.degrees(yaw)

    def getOrientation(self) -> Tuple[float, float, float]:
        """return the current orientation of the drone in degrees

        Returns:
            Tuple[float, float, float]: orientation (roll, pitch, yaw) of the drone in degrees, ranges from -180.0 to 180.0
        """
        orientation_quat = self.client.simGetVehiclePose().orientation
        orientation = airgen.to_eularian_angles(orientation_quat)
        return [np.degrees(orient) for orient in orientation]

    def simGetDepthImageFromCamera(
        self, camera_name: str
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """return the depth image of camera (camera_name) with the drone's current position and pose

        Args:
            camera_name (str): name of the camera, one of `front_center` or `bottom_center`

        Returns:
            Tuple[np.ndarray, Dict[str, Any]]: depth image represented by numpy array (float) of shape image array H X W X 1, parameters of the camera that capture the image
        """
        responses = self.client.simGetImages(
            [
                airgen.ImageRequest(
                    camera_name,
                    ImageType.DepthPerspective,
                    True,
                    False,
                )
            ]
        )
        response = responses[0]
        depth_img_in_meters = airgen.list_to_2d_float_array(
            response.image_data_float, response.width, response.height
        )
        depth_img_in_meters = depth_img_in_meters.reshape(
            response.height, response.width, 1
        )
        camera_param = {
            "width": response.width,
            "height": response.height,
            "camera_position": np.array(
                [
                    response.camera_position.x_val,
                    response.camera_position.y_val,
                    response.camera_position.z_val,
                ]
            ),
            "camera_orientation": list(
                map(
                    math.degrees, airgen.to_eularian_angles(response.camera_orientation)
                )
            ),
            "camera_quaternion_wxyz": (
                response.camera_orientation.w_val,
                response.camera_orientation.x_val,
                response.camera_orientation.y_val,
                response.camera_orientation.z_val,
            ),
            "fov": self.camera_info_extra[camera_name]["fov"],
        }
        return depth_img_in_meters, camera_param

    def simGetImages(
        self, camera_name: str, image_types: List[str]
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """return the images of camera(camera_name) with the drone's current position and pose

        Args:
            camera_name (str): name of the camera, one of `front_center` or `bottom_center`
            image_types [List[str]]: supported image types ["rgb", "depth", "segmentation"]
        Returns:
            Tuple[List[np.ndarray], Dict[str, Any]: requested images parameters of the camera that capture the image

        example:
        >>> images, camera_param = drone.simGetImages("front_center", ["rgb", "depth", "segmentation"])
        >>> rgb = images[0] # of shape (H, W, 3)
        >>> depth = image[1] # of shape (H, W, 1)
        >>> segmentation = image[2] # of shape (H, W, 1)
        """
        # assume all image types share the same set intrinsic parameters: width, height, and fov
        image_requests = [
            imagetype2request(camera_name=camera_name, image_type=AIRGEN_IMAGE_TYPE[t])
            for t in image_types
        ]
        responses = self.client.simGetImages(image_requests)
        images, camera_param = responses2image(
            responses, [AIRGEN_IMAGE_TYPE[t] for t in image_types]
        )
        camera_param["fov"] = self.camera_info_extra[camera_name]["fov"]
        return images, camera_param
