from typing import Tuple, Dict, Any, List, Optional
import os
import math
import logging
import time
import numpy as np
from PIL import Image
import rerun as rr
import airgen
from grid.model.model import Model, modelregistry

from grid.utils.airgen_utils.airgen_geometry import (
    depth2pointcloud,
    estimate_pointcloud_normals,
    vec2eulerangles,
    rotate_xy,
)
from grid.utils.airgen_utils.airgen_plot import mask_annotate

from grid import logger as grid_logger

logger = grid_logger


def segment_object(
    segmentation_model,
    rgbimage: np.ndarray,
    object_prompt: str,
    log_to_rr: bool = False,
):
    """segment object of interest

    Args:
        segmentation_model (Model): segmentation model
        rgbimage (np.ndarray): shape (width, height, 3)
        object_prompt (str): object of interest
        log_to_rr (bool): log images to rerun

    Returns:
        np.ndarray: segmentation mask, shape (width, height)
    """
    if log_to_rr:
        rr.log_image("inspection/rgbimage", rgbimage)
    segs = segmentation_model.run(rgbimage, object_prompt)
    if len(segs) == 0:
        logging.info("%s was not detected", object_prompt)
        return None
    # suppose there is only one object object_prompt
    seg_mask = segs[0][0]
    if log_to_rr:
        rr.log_segmentation_image("inspection/seg_mask", seg_mask)
    return seg_mask


def find_rightmost_point_cloud(
    camera_position: np.ndarray,
    image_width: int,
    point_cloud: np.ndarray,
    seg_mask: np.ndarray,
) -> Tuple[int, bool]:
    """Find index of the rightmost (in camera coordinate) point cloud on the same horizontal plane as camera/drone, and check the cooresponding pixel in seg_mask is close to the right boundary of the image

    Args:
        camera_position (np.ndarray):  np.array([x, y, z])
        image_width (int): _description_
        point_cloud (np.ndarray): _description_
        seg_mask (np.ndarray): _description_

    Returns:
        Tuple[np.ndarray, bool]:
            int: index of the rightmost point cloud
            bool: if the rightmost point cloud is close to the right boundary of the image
    """

    # todo: make this robust to noise and error in segmentation mask, and point cloud data
    hit_image_right_boundary = False
    # magic number is used 5 meters to find point cloud on the same horizontal plane as camera/drone
    # maybe find the closest 5 points
    indices_of_pc_horizontally_close = np.where(
        np.abs(point_cloud[:, 2] - camera_position[2]) < 5
    )

    # index map between seg_mask (2d) and point cloud (1d)
    index_map = np.where(seg_mask.squeeze(-1) > 0.5)

    indices_of_point_cloud_pixels = (
        index_map[0][indices_of_pc_horizontally_close],
        index_map[1][indices_of_pc_horizontally_close],
    )
    max_col_index = np.argmax(indices_of_point_cloud_pixels[1])
    max_col_val = indices_of_point_cloud_pixels[1][max_col_index]
    # col index starts with 0, so the maximum col value is image_width - 1
    # magic number 3 is used here
    hit_image_right_boundary = (image_width - 1 - max_col_val) < 3

    # find the corresponding point cloud
    index_of_rightmost_pc = indices_of_pc_horizontally_close[0][max_col_index]
    return index_of_rightmost_pc, hit_image_right_boundary


def test_find_rightmost_point_cloud():
    data_dir = os.path.abspath("./data")
    img_path = os.path.join(data_dir, "rgb.png")
    rgb_image = np.asarray(Image.open(img_path).convert("RGB"))
    depth_image = np.load(os.path.join(data_dir, "depth.npy"))
    seg_mask = np.load(os.path.join(data_dir, "seg_mask.npy"))
    seg_mask = np.expand_dims(seg_mask, axis=-1)
    rr.log_image("inspection/seg_mask", seg_mask)
    camera_param = {
        "fov": 90,
        "width": 256,
        "height": 256,
        "camera_position": np.array([111.21, 0.4, -49.665]),
        "camera_orientation": [
            17.63,
            -1.63e-05,
            -7.52e-05,
        ],
        "camera_quaternion_wxyz": [
            0.9926820993423462,
            4.4390273501448974e-07,
            0.15075699120759964,
            -7.330698281293735e-06,
        ],
    }
    point_cloud = depth2pointcloud(depth_image, camera_param, seg_mask)
    rr.log_points("inspection/point_cloud", point_cloud)
    find_rightmost_point_cloud(
        camera_param["camera_position"], 256, point_cloud, seg_mask
    )


def get_point_cloud_for_object(
    seg_mask: np.ndarray,
    depth_image: np.ndarray,
    camera_param: Dict[str, Any],
    log_to_rr: bool = False,
) -> Tuple[np.ndarray, np.ndarray]:
    """generate point cloud based on object delineated in seg_mask

    Args:
        seg_mask (np.ndarray): boolean mask of shape (H, W, 1)
        depth_image (np.ndarray): depth image (float) of shape (H, W, 1)
        camera_param (Dict[str, Any]): _description_
        log_to_rr (bool): _description_
    Returns:
        Tuple[np.ndarray, np.ndarray]: _description_
    """
    if log_to_rr:
        rr.log_depth_image("inspection/depthimage", depth_image)
        rr.log_segmentation_image("inspection/seg_mask", seg_mask)

    # suppose there is only one object object_prompt
    # seg_mask = filter_segment_mask(depthimage=depthimage, segment_mask=segs[0][0])
    # if model.logging:
    #     rr.log_segmentation_image("turbine/seg_mask", seg_mask)
    point_cloud = depth2pointcloud(depth_image, camera_param, seg_mask)
    point_cloud_normal = estimate_pointcloud_normals(point_cloud)
    if log_to_rr:
        rr.log_points("inspection/point_cloud", point_cloud)
    return point_cloud, point_cloud_normal


@modelregistry.register_model(name="nav-inspect")
class ObjectInspect(Model):
    """objection inspection model, plan path for inspecting object"""

    def __init__(self) -> None:
        super().__init__()
        self.inspect_resolution = 0.02  # meter per pixel
        self.logging = True

    def generate_poses_for_object_inspection(
        self,
        seg_mask: np.ndarray,
        depth_image: np.ndarray,
        camera_param: dict,
    ) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """plant points near object surface for inspection where the object is delineated by the segmenation mask

        Args:
            seg_mask (np.ndarray): boolean np.array shape (H, W, 3)
            depth_image (np.ndarray): shape (H, W, 1)
            camera_param (dict): parameters of camera that take the depth image

        Returns:
            Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
                Optional[np.ndarray]: positions of inspection points, shape (N, 3). None if object is not detected
                Optional[np.ndarray]: eular angles (pitch, roll, yaw in degrees) for inspection each each position, shape (N, 3). None if object is not detected

        Example:
        >>> positions, angles = self.generate_poses_for_object_inspection(rgb, depth, camera_param, "turbine")
        >>> if positions is None:
        >>>     for i, position in enumerate(positions):
        >>>         drone.simMoveToPosition(position)
        >>>         drone.simSetYaw(angles[i][2]) # angles[i] represents (pitch, roll, yaw) in degrees
        """

        point_cloud, point_cloud_normal = get_point_cloud_for_object(
            seg_mask, depth_image, camera_param, self.logging
        )
        inspect_focal_view_range = self.inspect_resolution * camera_param["width"]
        # distance from camera to the inspection point on the object surface
        inspect_distance = (
            0.5
            * inspect_focal_view_range
            / math.tan(math.radians(camera_param["fov"] / 2))
        )
        # extra step to filter normals
        point_cloud_normal = align_point_cloud_normals(
            point_cloud,
            point_cloud_normal,
            camera_param["camera_position"],
        )
        inspect_positions = point_cloud + point_cloud_normal * inspect_distance
        if self.logging:
            rr.log_points("inspection/inspect_positions", inspect_positions)

        if self.logging:
            rr.log_points("inspection/inspect_positions_aligned", inspect_positions)
            for i in range(inspect_positions.shape[0]):
                rr.log_arrow(
                    f"inspection/arrows_aligned/inspect_camera_orientations_{i}",
                    inspect_positions[i],
                    -point_cloud_normal[i],
                )
        inspect_camera_angles = vec2eulerangles(-point_cloud_normal)
        return inspect_positions, inspect_camera_angles

    def generate_next_viewpoint(
        self,
        seg_mask: np.ndarray,
        depth_image: np.ndarray,
        camera_param: dict,
        view_distance: Optional[float] = None,
    ) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """generate the next (counter-clockwise) viewpoint world coordinate.

        Args:
            seg_mask (np.ndarray): shape (H, W, 1)
            depth_image (np.ndarray): shape (H, W, 1)
            camera_param (dict): parameters of camera that take the rgb and depth image
            view_distance (float): distance from camera to the vantage point

        Returns:
            Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
                Optional[np.ndarray]: position of the next view points in world coordinate, of shape (N, 3).
                Optional[np.ndarray]: angles in degrees (pitch, roll, yaw) of vantage points in world coordinate of shape (N, 3).
        """
        point_cloud, point_cloud_normal = get_point_cloud_for_object(
            seg_mask, depth_image, camera_param
        )

        # check if right-most points (on the same horizontal plane) are close to image's right boundary (in image plane)
        camera_position = camera_param["camera_position"]

        index_of_rightmost_pc, hit_image_right_boundary = find_rightmost_point_cloud(
            camera_position, camera_param["width"], point_cloud, seg_mask
        )
        rightmost_pc = point_cloud[index_of_rightmost_pc]
        if view_distance is None:
            view_distance = np.linalg.norm(rightmost_pc - camera_position)
        if hit_image_right_boundary:
            logger.warn("hit image right boundary")
            rightmost_pc_normal = point_cloud_normal[index_of_rightmost_pc]
            # todo: check if normal is normalized
            return rightmost_pc + rightmost_pc_normal * view_distance, vec2eulerangles(
                np.expand_dims(-rightmost_pc_normal, axis=0)
            ).squeeze(axis=0)
        else:
            logger.info("did not hit image right boundary")
            # next view point face towards the right most point
            # view direction is perpendicular to vector (current view point, right most point)
            rr.log_point("inspection/current_viewpoint", camera_position)
            # airgen use ned coordinate system, so we do not need to flip the sign of direction
            view_direction = rotate_xy(
                camera_position - rightmost_pc, 90
            )  # todo: pertube? make it more robust
            view_direction = view_direction / np.linalg.norm(view_direction)
            rr.log_arrow(
                "inspection/view_direction",
                rightmost_pc - view_distance * view_direction,
                rightmost_pc,
            )
            return rightmost_pc - view_distance * view_direction, vec2eulerangles(
                np.expand_dims(view_direction, axis=0)
            ).squeeze(axis=0)


def filter_segment_mask(depthimage: np.ndarray, segment_mask) -> np.ndarray:
    """filter segmentation mask with depth information

    Args:
        depthimage (_type_): shape (H, W, 1)
        segment_mask (_type_): _description_

    Returns:
        np.ndarray: shape (H, W)
    """
    object_depth = np.median(depthimage[segment_mask])
    # todo: remove the magic number 10.0 error torlerance parameter
    rr.log_segmentation_image("turbine/seg_mask_before_filter", segment_mask)
    segment_mask = np.where(
        np.logical_and(
            segment_mask == 1, np.abs(depthimage.squeeze(axis=-1) - object_depth) < 10
        ),
        True,
        False,
    )
    # rr.log_segmentation_image("turbine/seg_mask_after", segment_mask)
    return segment_mask


def align_point_cloud_normals(
    point_cloud: np.ndarray,
    estimated_point_cloud_normal: np.ndarray,
    camera_position: np.ndarray,
) -> np.ndarray:
    """align estimated pointcloud normal, flip the sign of those whose normal is not aligned with camera view direction

    Args:
        point_cloud (np.ndarray): (N, 3)
        estimated_point_cloud_normal: (np.ndarray): (N, 3)
        camera_position (np.ndarray): (3,)

    Returns:
        np.ndarray: aligned point cloud normals (N, 3)
    """
    view_vector = point_cloud - camera_position

    # perform dot/inner product over the column dimension
    mask = np.sum(view_vector * estimated_point_cloud_normal, axis=1) > 0
    estimated_point_cloud_normal[mask] = -estimated_point_cloud_normal[mask]
    return estimated_point_cloud_normal


def set_SegmentationId(airgen_drone, object_name):
    airgen_drone.client.simSetSegmentationObjectID("[\w]*", 0, True)
    time.sleep(1)
    airgen_drone.client.simSetSegmentationInstanceID(object_name, 1, False)
    time.sleep(1)
    # temporary fix to the issue of first segmentation image being abnormal
    airgen_drone.simGetImages("front_center", ["segmentation"])


def test_next_viewpoint():
    "test next viewpoint generation"
    drone = AirGenDrone()
    set_SegmentationId(drone, "StaticMeshActor_1")
    # anchor point to view the static turbine
    drone.velocity = 3.0
    drone.simMoveToPosition((110, 0, -50))
    time.sleep(1)

    objinsp = ObjectInspect()
    for i in range(6):
        images, camera_param = drone.simGetImages(
            "front_center", ["rgb", "depth", "segmentation"]
        )
        rgb_image = images[0]
        rr.log_image(f"inspection/rgbimage_{i}", rgb_image)
        depth_image = images[1]
        seg_mask = images[2]
        next_viewpoint, next_viewpoint_angles = objinsp.generate_next_viewpoint(
            seg_mask,
            depth_image,
            camera_param,
        )
        if True:
            next_viewpoint = next_viewpoint.tolist()
            next_viewpoint_angles = next_viewpoint_angles.tolist()

            drone.client.simPlotPoints(
                [
                    airgen.Vector3r(
                        x_val=next_viewpoint[0],
                        y_val=next_viewpoint[1],
                        z_val=next_viewpoint[2],
                    )
                ],
                size=10.0,
                duration=10.0,
                is_persistent=True,
            )

        drone.simMoveToPosition(
            (next_viewpoint[0], next_viewpoint[1], next_viewpoint[2])
        )
        drone.simSetYaw(next_viewpoint_angles[2])
        print(f"scanning at {i}th viewpoint")
        time.sleep(2)


def test_inspection(logging_in_airgen=False):
    drone = AirGenDrone()
    set_SegmentationId(drone, "StaticMeshActor_1")
    # anchor point to view the static turbine
    drone.velocity = 3.0
    drone.simMoveToPosition((110, 0, -50))
    time.sleep(1)
    drone.velocity = 1.0
    images, camera_param = drone.simGetImages(
        "front_center", ["rgb", "depth", "segmentation"]
    )
    rgb_image = images[0]
    rr.log_image("inspection/rgbimage", rgb_image)
    depth_image = images[1]
    seg_mask = images[2]
    objinsp = ObjectInspect()
    inspect_positions, inspect_poses = objinsp.generate_poses_for_object_inspection(
        seg_mask,
        depth_image,
        camera_param,
    )
    if inspect_positions is None:
        return
    if logging_in_airgen:
        inspect_positions = inspect_positions.tolist()
        inspect_poses = inspect_poses.tolist()
        for inspect_position in inspect_positions:
            drone.client.simPlotPoints(
                [
                    airgen.Vector3r(
                        x_val=inspect_position[0],
                        y_val=inspect_position[1],
                        z_val=inspect_position[2],
                    )
                ],
                size=10.0,
                duration=10.0,
                is_persistent=True,
            )

    for i in range(len(inspect_positions)):
        drone.simMoveToPosition(
            (inspect_positions[i][0], inspect_positions[i][1], inspect_positions[i][2])
        )
        drone.simSetYaw(inspect_poses[i][2])


if __name__ == "__main__":
    from grid.robot.airgen_drone import AirGenDrone

    # vantagerun()
    # test_vec2eulerangles()
    test_next_viewpoint()
    # test_inspection(logging_in_airgen=True)
    # test_eular_to_quat()
    # inspection(logging_in_airgen=True)
    # test_find_rightmost_point_cloud()
