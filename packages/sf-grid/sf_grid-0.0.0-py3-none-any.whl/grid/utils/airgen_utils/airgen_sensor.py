from typing import Callable, List, Any
import math
import os
import numpy as np
import airgen
import logging
import cv2


def segmask2bbox(seg_mask: np.ndarray) -> np.ndarray:
    """return a list of bounding box based segmentation mask.
    Note:
        1. assume background is 0
        2. each non-zero unique value in the segmentation mask is a unique object

    Args:
        seg_mask (np.ndarray): segmentation mask of shape (H, W)

    Returns:
        np.ndarray: a list of bounding box in (xyxy) format, shape (N, 4)
    """
    # seg_mask = cv2.erode(seg_mask, np.ones((5, 5), np.uint8), iterations=1)
    # seg_mask = cv2.dilate(seg_mask, np.ones((5, 5), np.uint8), iterations=1)
    segIDs = np.unique(seg_mask)
    bbox = []
    for i, idx in enumerate(segIDs):
        if idx == 0:
            # background
            continue
        y_coord, x_coord = np.where(seg_mask == idx)
        min_x, min_y, max_x, max_y = (
            np.min(x_coord),
            np.min(y_coord),
            np.max(x_coord),
            np.max(y_coord),
        )
        if (max_x - min_x) * (max_y - min_y) < 100:
            # ignore small objects
            continue
        bbox.append([min_x, min_y, max_x, max_y])
    return np.array(bbox, dtype=np.int32)


def imagetype2request(camera_name: str, image_type: str) -> airgen.ImageRequest:
    """return airgen image request for image type

    Args:
        camera_name (str): _description_
        image_type (str): _description_

    Returns:
        airgen.ImageRequest: _description_
    """
    if image_type in [airgen.ImageType.Scene, airgen.ImageType.Segmentation]:
        # uint8 type of data
        return airgen.ImageRequest(camera_name, image_type, False, False)
    else:
        # float type of data
        return airgen.ImageRequest(camera_name, image_type, True, False)


# utility function for post-processing of airgen sensor ouputs
def responses2image(responses: List[Any], image_types: List[str]) -> List[np.ndarray]:
    res = []
    for response, image_type in zip(responses, image_types):
        if image_type == airgen.ImageType.Scene:
            img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img1d.reshape(response.height, response.width, 3)
            img_rgb = img_rgb[:, :, ::-1]
            res.append(img_rgb)
        elif image_type == airgen.ImageType.DepthPerspective:
            depth_img_in_meters = airgen.list_to_2d_float_array(
                response.image_data_float, response.width, response.height
            )
            depth_img_in_meters = depth_img_in_meters.reshape(
                response.height, response.width, 1
            )
            res.append(depth_img_in_meters)
        elif image_type == airgen.ImageType.Segmentation:
            img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
            img_seg = img1d.reshape(response.height, response.width, 3)
            global SEGRGB2SEGID
            if SEGRGB2SEGID is None:
                SEGRGB2SEGID = read_airgen_segRGB2segID_mapping()
            res.append(SEGRGB2SEGID(img_seg))
        else:
            raise NotImplementedError(f"image type {image_type} not implemented")
    response = responses[0]
    camera_params = {}
    camera_params["width"] = response.width
    camera_params["height"] = response.height
    camera_params["camera_position"] = [
        response.camera_position.x_val,
        response.camera_position.y_val,
        response.camera_position.z_val,
    ]
    camera_params["camera_orientation"] = (
        list(map(math.degrees, airgen.to_eularian_angles(response.camera_orientation))),
    )
    camera_params["camera_quaternion_wxyz"] = [
        response.camera_orientation.w_val,
        response.camera_orientation.x_val,
        response.camera_orientation.y_val,
        response.camera_orientation.z_val,
    ]
    return res, camera_params


def regenerate_segRGB2segID_mapping():
    import csv
    import time

    client = airgen.VehicleClient(timeout_value=7200)
    client.confirmConnection()

    requests = airgen.ImageRequest("0", airgen.ImageType.Segmentation, False, False)

    # for
    colors = {}
    for cls_id in range(256):
        # map every asset to cls_id and extract the single RGB value produced
        client.simSetSegmentationObjectID("[\w]*", cls_id, is_name_regex=True)
        time.sleep(2)
        response = client.simGetImages([requests])[0]
        img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(response.height, response.width, 3)
        img_rgb = img_rgb[:, :, ::-1]
        # color = tuple(np.unique(img_rgb.reshape(-1, img_rgb.shape[-1]), axis=0)[1])
        # in the env currently being tested, the sky is always 0
        color = tuple(img_rgb[-1, -1, :])
        print(f"{cls_id}\t{color}")
        colors[cls_id] = color

    from grid import GRIDConfig

    segid_txt_path = GET_SEGRGB2SEGID_TXT_PATH(GRIDConfig.get_main_dir())
    with open(segid_txt_path, "w") as f:
        writer = csv.writer(f, delimiter=" ", lineterminator="\n")
        for k, v in colors.items():
            writer.writerow([k] + list(v))


def read_airgen_segRGB2segID_mapping() -> Callable:
    def rgb2segid(segRGB: np.ndarray) -> np.ndarray:
        """turn segmentation image represented by rgb to segmentation filled by segmentation ID


        Args:
            segRGB (np.ndarray): (H, W, 3) segmentation image represented by rgb

        Returns:
            np.ndarray: (H, W, 1)
        """
        segID = np.zeros((segRGB.shape[0], segRGB.shape[1], 1), dtype=np.uint8)
        # todo: vectorize this!
        for i in range(segRGB.shape[0]):
            for j in range(segRGB.shape[1]):
                id = segRGB2segID_mapping.get(tuple(segRGB[i, j]), 256)

                # sc: unrecognized color channel is probably for segmentationID=-1?
                if id == 256:
                    logging.info(
                        "RGB value not found in mapping: %s, and it set to 255",
                        str(segRGB[i, j]),
                    )
                    segID[i, j, 0] = 255
                else:
                    segID[i, j, 0] = id
        return segID

    from grid import GRIDConfig

    segid_txt_path = GET_SEGRGB2SEGID_TXT_PATH(GRIDConfig.get_main_dir())

    segRGB2segID_mapping = {}
    with open(segid_txt_path, "r") as f:
        for line in f.readlines():
            if line.strip() == "":
                continue
            segid, r, g, b = tuple(map(int, line.strip().split(" ")))
            segRGB2segID_mapping[(r, g, b)] = segid
    return rgb2segid


GET_SEGRGB2SEGID_TXT_PATH = lambda x: os.path.join(x, "data", "txt", "seg_colors.csv")
SEGRGB2SEGID = None

if __name__ == "__main__":
    sefRGB2segID = read_airgen_segRGB2segID_mapping()
    rgb = np.zeros((4, 3, 3), dtype=np.uint8)
    print(sefRGB2segID(rgb))
