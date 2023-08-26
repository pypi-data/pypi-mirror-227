from typing import Tuple, List
import numpy as np
import airgen
from .airgen_generic import airgenClient


def mask_annotate(mask, image):
    """overlap segmentation mask to rgb image

    Args:
        mask (np.ndarray): segmentation mask of shape (H, W)
        image (np.ndarray): rgb image of shape (H, W, 3)

    Returns:
        np.ndarray: rgb image with segmentation mask overlapped
    """
    from supervision.draw.color import ColorPalette

    opacity = 0.5
    colored_mask = np.zeros_like(image, dtype=np.uint8)
    color = ColorPalette.default().by_idx(0)
    colored_mask[:] = color.as_bgr()
    scene = np.where(
        np.expand_dims(mask, axis=-1),
        np.uint8(opacity * colored_mask + (1 - opacity) * image),
        image,
    )
    return scene


def plot_points_in_airgen(airgen_client, points: np.ndarray):
    """plot points persistantly in airgen

    Args:
        points (np.ndarray): of shape (N, 3)
    """

    points = points.tolist()
    client = airgenClient()
    airgen_client.simPlotPoints(
        [
            airgen.Vector3r(
                x_val=points[i][0],
                y_val=points[i][1],
                z_val=points[i][2],
            )
            for i in range(len(points))
        ],
        size=10.0,
        duration=10.0,
        is_persistent=True,
    )


def simPlot3DBox(
    airgen_client: airgen.VehicleClient,
    min_3dcoord: Tuple[float, float, float],
    max_3dcoord: Tuple[float, float, float],
) -> None:
    """Plot a 3d box in airgen simulator given the min and max 3d coordinates

    Args:
        airgen_client (airgen.VehicleClient): airgen client
        min_3dcoord (Tuple(float, float, float)): min 3d coordinate of the box
        max_3dcoord (Tuple(float, float, float)): max 3d coordinate of the box

    """
    min_x, min_y, min_z = min_3dcoord[0], min_3dcoord[1], min_3dcoord[2]
    max_x, max_y, max_z = max_3dcoord[0], max_3dcoord[1], max_3dcoord[2]

    airgen_client.simPlotPoints(
        [
            airgen.Vector3r(
                x_val=min_3dcoord[0], y_val=min_3dcoord[1], z_val=min_3dcoord[2]
            ),
            airgen.Vector3r(
                x_val=max_3dcoord[0], y_val=max_3dcoord[1], z_val=max_3dcoord[2]
            ),
        ],
        size=30.0,
        duration=10.0,
        is_persistent=True,
    )
    # Define the 8 corners of the box
    p1 = airgen.Vector3r(min_x, min_y, min_z)
    p2 = airgen.Vector3r(min_x, min_y, max_z)
    p3 = airgen.Vector3r(min_x, max_y, min_z)
    p4 = airgen.Vector3r(min_x, max_y, max_z)
    p5 = airgen.Vector3r(max_x, min_y, min_z)
    p6 = airgen.Vector3r(max_x, min_y, max_z)
    p7 = airgen.Vector3r(max_x, max_y, min_z)
    p8 = airgen.Vector3r(max_x, max_y, max_z)

    lines = [
        p1,
        p2,
        p1,
        p3,
        p1,
        p5,
        p2,
        p4,
        p2,
        p6,
        p3,
        p4,
        p3,
        p7,
        p4,
        p8,
        p5,
        p6,
        p5,
        p7,
        p6,
        p8,
        p7,
        p8,
    ]

    airgen_client.simPlotLineList(lines, thickness=10.0, is_persistent=True)
