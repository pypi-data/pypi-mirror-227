import os
from typing import List, Tuple

import cv2
import numpy as np
import supervision as sv
import torch
from PIL import Image
import torchvision
from groundingdino.util.inference import Model as gdino_model
from PIL import Image
from segment_anything import SamPredictor, sam_model_registry
import rerun as rr
from grid.model.model import Model, modelregistry

SAM_CHECKPOINTS = {
    "h": ("vit_h", "sam_vit_h_4b8939.pth"),
    "l": ("vit_l", "sam_vit_l_0b3195.pth"),
    "b": ("vit_b", "sam_vit_b_01ec64.pth"),
}
SAM_MODEL_SIZE = "b"


@modelregistry.register_model(name="seg-gsam")
class GroundedSAM(Model):
    BOX_THRESHOLD = 0.4
    TEXT_THRESHOLD = 0.25
    NMS_THRESHOLD = 0.8

    _static_model_sam = None
    _static_model_gdino = None

    def __init__(self) -> None:
        """Initialize groundingdino model."""
        super().__init__()
        from grid import GRIDConfig

        if GroundedSAM._static_model_sam is None:
            model_data_dir = os.path.join(
                GRIDConfig.get_main_dir(), "external", "model_weights"
            )
            sam = sam_model_registry[SAM_CHECKPOINTS[SAM_MODEL_SIZE][0]](
                checkpoint=os.path.join(
                    model_data_dir, SAM_CHECKPOINTS[SAM_MODEL_SIZE][1]
                )
            )
            GroundedSAM._static_model_sam = SamPredictor(sam)
            GroundedSAM._static_model_gdino = gdino_model(
                model_config_path=os.path.join(
                    model_data_dir, "GroundingDINO_SwinT_OGC.py"
                ),
                model_checkpoint_path=os.path.join(
                    model_data_dir, "groundingdino_swint_ogc.pth"
                ),
            )

    def run(
        self, rgbimage: np.ndarray, text_prompt: str
    ) -> Tuple[np.ndarray, np.int64, float]:
        """detect and segment objects from rgbimage where the target objects are specificed by text_prompt

        Args:
            rgbimage (np.ndarray): target rgb image represented as numpy array of shape (H, W, 3)
            text_prompt (str): text prompt specifies the objects to be detected and segmented.

        Returns:
            Tuple[np.ndarray, np.int64, float]:
                object mask (np.ndarray): object pixels are 1, others 0
                class_id (np.int64)
                confidence (float): confidence of segmentation

            Example:
            >>> gsam = GroundSAM()
            >>> res = gsam.run(img, "turbine")
        """

        # gdino model.predict_with_class assumes input image is bgr
        detections = GroundedSAM._static_model_gdino.predict_with_classes(
            image=cv2.cvtColor(rgbimage, cv2.COLOR_RGB2BGR),
            classes=[text_prompt],
            box_threshold=self.BOX_THRESHOLD,
            text_threshold=self.TEXT_THRESHOLD,
        )

        # NMS post process to remove overlapping boxes
        nms_idx = (
            torchvision.ops.nms(
                torch.from_numpy(detections.xyxy),
                torch.from_numpy(detections.confidence),
                self.NMS_THRESHOLD,
            )
            .numpy()
            .tolist()
        )

        detections.xyxy = detections.xyxy[nms_idx]
        detections.confidence = detections.confidence[nms_idx]
        detections.class_id = detections.class_id[nms_idx]

        detections.mask = segment(
            sam_predictor=GroundedSAM._static_model_sam,
            image=rgbimage,
            xyxy=detections.xyxy,
        )
        res = [
            (detections.mask[i], detections.class_id[i], detections.confidence[i])
            for i in range(len(detections.mask))
        ]
        return res


def segment(sam_predictor, image: np.ndarray, xyxy: np.ndarray) -> np.ndarray:
    sam_predictor.set_image(image)
    result_masks = []
    for box in xyxy:
        masks, scores, logits = sam_predictor.predict(box=box, multimask_output=True)
        index = np.argmax(scores)
        result_masks.append(masks[index])
    return np.array(result_masks)


if __name__ == "__main__":
    rr.init("gsam/turbine")
    img_path = "./data/image/turbine.png"
    # read image
    img = np.asarray(Image.open(img_path).convert("RGB"))
    rr.log_image("rgbimage", img)
    gdinotool = GroundedSAM()
    seg = gdinotool.run(img, "turbine")
    print(seg)
