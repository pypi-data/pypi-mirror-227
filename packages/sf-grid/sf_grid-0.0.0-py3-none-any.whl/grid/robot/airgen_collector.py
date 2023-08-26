"""Implement drone in AirGen environment
    every angle in-out of this class is in degrees
"""
from typing import List, Dict, Any, Tuple
import math
import os
import time
import logging
import numpy as np
import airgen
from airgen.types import ImageType
import rerun as rr
from grid.registry import registry
from grid.robot.robot import Robot


from grid.utils.airgen_utils.airgen_sensor import (
    responses2image,
    imagetype2request,
    segmask2bbox,
)
from grid.utils.airgen_utils.airgen_plot import simPlot3DBox
from grid.utils.airgen_utils.airgen_generic import airgenClient, vector3d2list
from grid.utils.airgen_utils.airgen_geometry import (
    cameracoord2worldcoord,
    vec2eulerangles,
)


# todo: coordinate origin fixed?

# notes:
# 1. two bbox each image: bigger one based on airgen side detection, smaller one based on segmentation mask
# 2. two turbines do not share the prefix in `actor_name`, hence detection results only show one of them


@registry.register_robot(name="airgencollector")
class AirGenCollector(Robot):
    prompt_prefix = "sim"

    def __init__(self) -> None:
        """Set up client and connect to airgen, and take off the drone."""
        # keep a log for monitoring behvaiors of the drone
        from grid import GRIDConfig

        self.logdir = os.path.join(
            os.path.dirname(GRIDConfig.get_main_dir()),
            f"log/collection",
        )
        os.makedirs(self.logdir, exist_ok=True)
        # connect to airgen
        self.client = airgenClient()
        self.client.confirmConnection()

        self.objects_in_scene = None
        self.camera_info = None
        self.min_pixels_for_object = 128
        self.setup()

    def setup(self) -> None:
        self.camera_info = {
            "front_center": self.getCameraInfo("front_center"),
            "bottom_center": self.getCameraInfo("bottom_center"),
        }
        # get all objects in the scene
        self.objects_in_scene = set(self.client.simListSceneObjects())

    def getCameraInfo(self, camera_name: str):
        info = self.client.simGetCameraInfo(camera_name)
        # print(info)
        return {"fov": info.fov}

    def simCollectImagesAroundObject(
        self,
        object_name: str,
        camera_name: str = "front_center",
        image_types: List[str] = [
            airgen.ImageType.Scene,
            airgen.ImageType.DepthPerspective,
            airgen.ImageType.Segmentation,
        ],
        num_images: int = 10,
    ) -> None:
        """given object name, collect annotaed images from around the object

        Args:
            object_name (str): name of the object
            camera_name (str, optional): name of the camera. Defaults to "front_center".
            image_types (List[str], optional): types of images to collect. Defaults to [airgen.ImageType.Scene, airgen.ImageType.DepthPerspective, airgen.ImageType.Segmentation].
            num_images (int, optional): number of images to collect. Defaults to 10.

        """
        # 1. get object coordinates and dimensions, sample points around the object
        # 2. determine the sample radius based on camera resolution and fov
        # 3. for each sample point, move the drone to the point, take a picture
        # 4. save the image, and information about the object
        # 5. add pre-post filter to remove images that do not contain (fullly) the object
        if object_name not in self.objects_in_scene:
            logging.warning("%s is not found in the scene", object_name)
            return
        self.client.simClearDetectionMeshNames(camera_name, airgen.ImageType.Scene)
        # get object coordinates and dimensions
        # todo: which to use as center
        # object_pose = self.client.simGetObjectPose(object_name)
        object_center = self.client.simGetObjectCenter(object_name)
        object_center = np.array(vector3d2list(object_center))
        rr.log_point(
            "points/object_center",
            position=object_center,
            radius=2,
        )
        object_dimensions = self.client.simGetObjectDimensions(object_name)
        self.client.simAddDetectionFilterMeshName(
            camera_name, airgen.ImageType.Scene, object_name
        )
        object_diamter = (
            np.linalg.norm(
                [
                    object_dimensions.x_val,
                    object_dimensions.y_val,
                    object_dimensions.z_val,
                ]
            )
            / 100
        )  # object diameter in [m]

        # compute distance range between camera and object, based on camera resolution and fov
        minimum_look_distance = (object_diamter / 2.0) / math.tan(
            math.radians(self.camera_info[camera_name]["fov"] / 2)
        )
        image_width = self.client.simGetImages(
            [airgen.ImageRequest(camera_name, ImageType.Scene, False, False)]
        )[0].width
        maximum_look_distance = (
            (object_diamter / self.min_pixels_for_object)
            * image_width
            / 2
            / math.tan(math.radians(self.camera_info[camera_name]["fov"] / 2))
        )
        maximum_look_distance = max(maximum_look_distance, 2 * minimum_look_distance)

        self.client.simSetDetectionFilterRadius(
            camera_name, airgen.ImageType.Scene, 2 * maximum_look_distance * 100
        )  # in [cm]
        time.sleep(1)

        self.client.simSetSegmentationObjectID("[\w]*", 0, True)
        time.sleep(1)
        self.client.simSetSegmentationInstanceID(object_name, 1, False)

        # temporary fix to the issue of first segmentation image being abnormal
        responses = self.client.simGetImages(
            [imagetype2request(camera_name, image_type) for image_type in image_types]
        )
        # object_id = self.client.simGetSegmentationObjectID(object_name.lower())
        # time.sleep(2)
        # print(f"{object_name} has object id {object_id}")
        num_collected_images = 0
        num_trials = 0
        while num_collected_images < num_images:
            num_trials += 1
            coordinate = sample_points_around_object(
                object_center, minimum_look_distance, maximum_look_distance, 1
            )[0]
            # move the drone to the point
            object_dir_vec = object_center - coordinate
            object_dir_ang = vec2eulerangles(
                np.expand_dims(object_dir_vec, axis=0)
            ).squeeze(0)
            target_pitch, target_yaw = object_dir_ang[0], object_dir_ang[2]
            self.client.simSetCameraPose(
                camera_name=camera_name,
                pose=airgen.Pose(
                    airgen.Vector3r(coordinate[0], coordinate[1], coordinate[2]),
                    # airgen.Quaternionr(),
                    airgen.to_quaternion(
                        math.radians(target_pitch), 0, math.radians(target_yaw)
                    ),
                ),
            )
            time.sleep(1)
            # take a picture
            responses = self.client.simGetImages(
                [
                    imagetype2request(camera_name, image_type)
                    for image_type in image_types
                ]
            )

            images, _ = responses2image(responses, image_types)

            # add pre-post filter to remove images that do not contain (fullly) the object

            detections = self.client.simGetDetections(
                camera_name, airgen.ImageType.Scene
            )

            bboxfromseg = segmask2bbox(images[airgen.ImageType.Segmentation])
            if len(bboxfromseg) == 0:
                logging.info(
                    "object %s is not visible in the %d-th segmentation image",
                    object_name,
                    num_trials,
                )
                continue
            num_collected_images += 1
            for j, box in enumerate(bboxfromseg):
                rr.log_rect(
                    f"image/camera_{num_collected_images}/rect_{j}_from_seg",
                    rect=box,
                    rect_format=rr.RectFormat.XYXY,
                )
            rr.log_point(
                f"points/camera_position_{num_collected_images}",
                position=coordinate,
                radius=1,
            )
            for image_type in image_types:
                if image_type == airgen.ImageType.DepthPerspective:
                    rr.log_depth_image(
                        f"image/camera_{num_collected_images}/depth", images[image_type]
                    )
                elif image_type == airgen.ImageType.Scene:
                    rr.log_image(
                        f"image/camera_{num_collected_images}/rgb", images[image_type]
                    )
                elif image_type == airgen.ImageType.Segmentation:
                    rr.log_segmentation_image(
                        f"image/camera_{num_collected_images}/segmentation",
                        images[image_type],
                    )
                else:
                    raise NotImplementedError("image type not implemented")
            if detections is None or len(detections) == 0:
                logging.info(
                    "object %s is not detected in the %d-th image",
                    object_name,
                    num_collected_images,
                )
                continue
            for j, detection in enumerate(detections):
                rr.log_rect(
                    f"image/camera_{num_collected_images}/rect_{j}",
                    rect=[
                        int(detection.box2D.min.x_val),
                        int(detection.box2D.min.y_val),
                        int(detection.box2D.max.x_val),
                        int(detection.box2D.max.y_val),
                    ],
                    rect_format=rr.RectFormat.XYXY,
                )
                # box3d_min = cameracoord2worldcoord(
                #     vector3d2list(detection.box3D.min), camera_params
                # ).tolist()
                # box3d_max = cameracoord2worldcoord(
                #     vector3d2list(detection.box3D.max), camera_params
                # ).tolist()
                # simPlot3DBox(self.client, box3d_min, box3d_max)


def sample_points_around_object(
    origin: np.ndarray, inner_radius: float, outer_radius: float, num_points: int
) -> np.ndarray:
    u = np.random.uniform(0, 1, num_points)
    v = np.random.uniform(0, 1, num_points)
    phi = 2 * np.pi * u
    theta = np.arccos(2 * v - 1)
    r = outer_radius * np.cbrt(
        np.random.uniform(inner_radius / outer_radius, 1, num_points)
    )

    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    sample_points = np.stack([x, y, z], axis=1)
    return sample_points + origin


def test_sample_points_around_object(origin, inner_radius, outer_radius, num_points):
    # curate a list of sample points around the object
    points = [
        [179.48804105, -48.03966227, -114.91311732],
        [200.04558456, 4.46319025, -116.35172968],
        [220.04558456, 4.46319025, -36.35172968],
        [
            145.14862015,
            44.91593895,
            35.55517214,
        ],  # bug on segmentation image, object is not visiable, but one pixel is labeled in seg
    ]
    res = np.array(points)
    return res


if __name__ == "__main__":
    rr.init("airgencollector", spawn=True)
    drone = AirGenCollector()
    drone.simCollectImagesAroundObject("StaticMeshActor_1")
    # test_3dbox()
