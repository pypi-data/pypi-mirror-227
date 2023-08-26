from typing import Tuple, Dict, Any, List, Optional
import math
import numpy as np
import torch
import ivy
import ivy_vision
import ivy_mech

# for some ivy version, it is `ivt.set_framework('numpy')`
if hasattr(ivy, "set_framework"):
    ivy.set_framework("numpy")
elif hasattr(ivy, "set_backend"):
    ivy.set_backend("numpy")
else:
    raise ValueError("ivy does not support set_framework or set_backend")
from pytorch3d.ops import (
    estimate_pointcloud_normals as estimate_pointcloud_normals_pytorch3d,
)

NP_FLOATING_TYPE = np.float32


def homo_coord_to_nonhome_coord(home_coord: ivy.Array) -> ivy.Array:
    """turn homogeneous coordinates to non-homogeneous coordinates

    Args:
        home_coord (ivy.Array): of shape (..., n)

    Returns:
        ivy.Array: of shape (..., n-1)
    """
    non_home_coord = home_coord / home_coord[..., -1][..., None]
    return non_home_coord[..., :-1]


def cameracoord2worldcoord(
    camera_coord: List[float], camera_params: dict
) -> np.ndarray:
    cam_inv_ext_mat = build_camera_inv_extrinsic(camera_params=camera_params)
    world_coord = ivy_vision.cam_to_world_coords(camera_coord, cam_inv_ext_mat)[
        ..., 0:3
    ]
    return world_coord


def quat_wxyz_to_xyzw(quat_wxyz):
    return np.array(
        [quat_wxyz[1], quat_wxyz[2], quat_wxyz[3], quat_wxyz[0]], dtype=NP_FLOATING_TYPE
    )


def build_camera_intrinsic(camera_params: dict) -> ivy_vision.Intrinsics:
    pp_offset = np.array(
        [item / 2 - 0.5 for item in [camera_params["width"], camera_params["height"]]],
        dtype=NP_FLOATING_TYPE,
    )
    persp_angle = np.array(
        [camera_params["fov"] * np.pi / 180] * 2, dtype=NP_FLOATING_TYPE
    )
    intrinsic = ivy_vision.persp_angles_and_pp_offsets_to_intrinsics_object(
        persp_angle, pp_offset, [camera_params["width"], camera_params["height"]]
    )
    return intrinsic


def build_camera_inv_extrinsic(camera_params: dict) -> ivy.Array:
    cam_position = np.array(camera_params["camera_position"], dtype=NP_FLOATING_TYPE)
    cam_quaternion = quat_wxyz_to_xyzw(camera_params["camera_quaternion_wxyz"])
    cam_quat_poses = ivy.concatenate((cam_position, cam_quaternion), axis=-1)

    cam_inv_ext_mat = ivy_mech.quaternion_pose_to_mat_pose(cam_quat_poses)
    return cam_inv_ext_mat


def build_camera(camera_params: dict):
    intrinsic = build_camera_intrinsic(camera_params)
    cam_inv_calib_mat = intrinsic.inv_calib_mats
    cam_inv_ext_mat = build_camera_inv_extrinsic(camera_params)
    return cam_inv_ext_mat, cam_inv_calib_mat


def camera_unproject_depth(
    depth: np.ndarray, cam_inv_ext_mat: ivy.Array, cam_inv_calib_mat: ivy.Array
) -> np.ndarray:
    """generate point cloud from depth image (depth perspective)

    Args:
        depth (np.ndarray): of shape (H, W, 1)
        cam_inv_ext_mat (ivy.Array): inverse of camera extrinsic matrix
        cam_inv_calib_mat (ivy.Array): inverse of camera intrinsic matrix

    Returns:
        np.ndarray: point cloud of shape (N, 3)
    """
    uniform_pixel_coords = ivy_vision.create_uniform_pixel_coords_image(
        image_dims=(depth.shape[0], depth.shape[1])
    )

    cam_coords = ivy_vision.ds_pixel_to_cam_coords(
        uniform_pixel_coords,
        cam_inv_calib_mat,
        [],
        image_shape=(depth.shape[0], depth.shape[1]),
    )
    # normalize the (non-homogeneous) part of camera coordinates to have unit norm and then scale by depth
    cam_coords[..., :-1] = (
        cam_coords[..., :-1]
        / np.linalg.norm(cam_coords[..., :-1], axis=-1, keepdims=True)
    ) * depth
    # camera coordinate to ned
    camera2ned = np.array(
        [[0, -1, 0, 0], [0, 0, -1, 0], [1, 0, 0, 0], [0, 0, 0, 1]],
        dtype=cam_coords.dtype,
    )
    # which is the transpose of
    # camera2ned = np.transpose(
    #     np.array(
    #         [[0, 0, 1, 0], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 1]],
    #         dtype=cam_coords.dtype,
    #     )
    # )
    ned_coords = np.dot(cam_coords, camera2ned)
    return ivy_vision.cam_to_world_coords(ned_coords, cam_inv_ext_mat)[..., 0:3]


def imagecoord2orientation(pixelcoord, camera_param):
    """Given camera parameters (position, pose, and fov) and  pixel coordinate, return the 3D direction of the pixel
    with respect to the camera represented in yaw and pitch (absolute degrees)

    Args:
        pixelcoord (Tuple[float, float]): coordinate of the pixel in the image in xy format
        camera_param (Dict[str, Any]): camera parameters

    Returns:
        Tuple[float, float]: yaw and pitch in degrees
    """
    delta_yaw = (
        (pixelcoord[0] - camera_param["width"] / 2)
        / camera_param["width"]
        * camera_param["fov"]
    )

    delta_pitch = (
        (camera_param["height"] / 2 - pixelcoord[1])
        / camera_param["height"]
        * 2
        * math.degrees(
            math.atan(
                math.tan(math.radians(camera_param["fov"] / 2))
                / (camera_param["width"] / camera_param["height"])
            )
        )
    )
    target_yaw, target_pitch = (
        math.radians(camera_param["camera_orientation"][2] + delta_yaw),
        math.radians(camera_param["camera_orientation"][0] + delta_pitch),
    )
    return (target_pitch, 0, target_yaw)


def imagecoord2direction(
    pixelcoord: Tuple[float, float], camera_param: Dict[str, Any]
) -> Tuple[float, float, float]:
    """Given camera parameters (position, pose, and fov) and  pixel coordinate, return the 3D direction of the pixel
    with respect to the camera

    Args:
        pixelcoord (Tuple[float, float]): coordinate of the pixel in the image in xy format
        camera_param (Dict[str, Any]): camera parameters

    Returns:
        Tuple[float, float, float]: normalized unit vector (x, y, z)
    """
    target_pitch, _, target_yaw = imagecoord2orientation(pixelcoord, camera_param)
    target_direction = pose2vector(target_pitch, 0, target_yaw)

    return target_direction


def pose2vector(pitch, roll, yaw):
    vector = [
        math.cos(pitch) * math.cos(yaw),
        math.cos(pitch) * math.sin(yaw),
        -math.sin(pitch),
    ]
    return vector


def imagecoord2pose(pixelcoord, point_depth, camera_param):
    """convert pixel coordinate to 3D coordinate"""
    target_pitch, _, target_yaw = imagecoord2orientation(pixelcoord, camera_param)
    target_direction = pose2vector(target_pitch, 0, target_yaw)
    target_coord = (
        np.array(target_direction) * point_depth + camera_param["camera_position"]
    )
    return target_coord, (target_pitch, 0, target_yaw)


def vec2eulerangles(vec: np.ndarray) -> np.ndarray:
    """transform directional vector to euler angles
    Params:
    vec: directional vector of shape (N, 3)
    """

    yaw = np.rad2deg(np.arctan2(vec[:, 1], vec[:, 0]))
    pitch = np.rad2deg(
        np.arctan2(-vec[:, 2], np.sqrt(np.square(vec[:, 0]) + np.square(vec[:, 1])))
    )
    return np.stack([pitch, np.zeros_like(pitch), yaw], axis=1)


def depth2pointcloud(
    depth: np.ndarray,
    camera_param: dict,
    mask: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """generating point cloud from depth image

    Args:
        depth (np.ndarray): depth image of shape (H, W, 1)
        camera_param (dict): camera parameters that contains fov, height, width and camera pose
        mask (Optional[np.ndarray], optional): boolean (0/1) mask where 1 indicates object of interest, (H, W, 1). Defaults to None.

    Returns:
        np.ndarray: point cloud in world coordinate of shape (N, 3)
    """

    camera_inv_ext_mat, camera_inv_calib_mat = build_camera(camera_param)
    point_cloud = camera_unproject_depth(
        depth=depth,
        cam_inv_ext_mat=camera_inv_ext_mat,
        cam_inv_calib_mat=camera_inv_calib_mat,
    )

    if mask is not None:
        point_cloud = point_cloud[np.where(mask.squeeze(-1) > 0.5)]

    point_cloud = point_cloud.reshape(-1, 3)

    return point_cloud


def test_index_mapping():
    seg_mask = np.random.random((2, 2, 1))
    print(seg_mask.squeeze(-1))
    # Generate a random point cloud array of the same shape for this example
    point_cloud = np.random.random((2, 2, 3))
    print(point_cloud)
    indices = np.where(seg_mask.squeeze(-1) > 0.5)
    print(indices)
    point_cloud = point_cloud[indices]
    print(point_cloud.shape)
    print(point_cloud)


def estimate_pointcloud_normals(point_cloud: np.ndarray, neighborhood_size: int = 10):
    """estimate point cloud normals

    Args:
        point_cloud (np.ndarray): point cloud of shape (N, 3)
        neighborhood_size (int, optional): neighborhood size to estimate local normas. Defaults to 10.

    Returns:
        np.ndarray: point cloud normals of shape (N, 3)

    """

    point_cloud_normals = estimate_pointcloud_normals_pytorch3d(
        torch.from_numpy(point_cloud).unsqueeze(0), neighborhood_size=neighborhood_size
    ).squeeze(0)
    return point_cloud_normals.numpy()


def rotate_xy(vec: np.ndarray, theta: float) -> np.ndarray:
    """rotate xy-component of 3d vector by theta (in degrees) counter-clockwise (in xy plane)
    Assume: looking from positive z-axis
        ^ y
        |
        |
        |______> x
    Args:
        vec (np.ndarray): shape (3,)
        theta (float): angles in degrees

    Returns:
        np.ndarray: rotated vector shape (3,)
    """
    theta_radians = math.radians(theta)
    rotation_matrix = np.array(
        [
            [math.cos(theta_radians), -math.sin(theta_radians), 0],
            [math.sin(theta_radians), math.cos(theta_radians), 0],
            [0, 0, 1],
        ],
        dtype=vec.dtype,
    )
    rotated_vec = np.dot(rotation_matrix, vec)
    return rotated_vec


if __name__ == "__main__":
    vec = np.array([1, 0, 0], dtype=np.float32)
    print(rotate_xy(vec, 90))
