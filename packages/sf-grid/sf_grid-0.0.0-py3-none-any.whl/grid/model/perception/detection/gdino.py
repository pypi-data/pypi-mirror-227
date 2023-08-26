import os
from typing import List, Tuple

import cv2
import groundingdino.datasets.transforms as T
import numpy as np
import torch
from groundingdino.util.inference import annotate, load_model, predict
from PIL import Image
from torchvision.ops import box_convert
from supervision.draw.color import ColorPalette
import rerun as rr
from grid.model.model import Model, modelregistry


@modelregistry.register_model(name="detection-gdino")
class GroundingDINO(Model):
    """Open-set object detector based on GoundingDINO."""

    BOX_TRESHOLD = 0.4
    TEXT_TRESHOLD = 0.25
    _static_model = None

    def __init__(self) -> None:
        """Initialize groundingdino model."""
        super().__init__()
        from grid import GRIDConfig

        if GroundingDINO._static_model is None:
            model_weights_dir = os.path.join(
                GRIDConfig.get_main_dir(),
                "external",
                "model_weights",
            )
            GroundingDINO._static_model = load_model(
                os.path.join(
                    model_weights_dir,
                    "GroundingDINO_SwinT_OGC.py",
                ),
                os.path.join(
                    model_weights_dir,
                    "groundingdino_swint_ogc.pth",
                ),
            )
        self._transform = T.Compose(
            [
                T.RandomResize([800], max_size=1333),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )
        self.frames = 0

        self.time_step = GRIDConfig.time_step

        self.logging = False

    def detect_object(
        self, rgbimage: np.ndarray, text_prompt: str
    ) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Detect objects, which is specified by the `text_prompt`, in the rgbimage and return the
        bounding boxe and phrases.

        Args:
            rgbimage (np.ndarray): target rgb image represented as numpy array of shape (H, W, 3)
            text_prompt (str): text prompt specifies the objects to be detected. There can be multiple objects in the prompt, and different objects are separated by `.`

        Returns:
            Tuple[np.ndarray, List[str]]:
                bounding boxes (np.ndarray): list of bounding boxes with 2D pixel coordinates with respect to the image in xyxy format. (N, 4).
                phrases (List[str]): list of object names corresponding to the boxes, (N)
            Example:
            >>> gdinomodel = GroundingDINO()
            >>> boxes, phrases = gdinomodel.detect_object(img, "dog . cake"")
        """
        if self.logging:
            rr.set_time_seconds("stable_time", self.frames * 0.01)
            rr.log_image("gdino/raw_image", rgbimage)
        # input array should be uint8 of size (H, W, 3)
        h, w, _ = rgbimage.shape
        rgbimage_image = Image.fromarray(rgbimage, mode="RGB")
        # rgbimage_image.save(f"rgbimage_{self.frames}.png")
        rgbimage_tensor, _ = self._transform(rgbimage_image, None)
        boxes, logits, phrases = predict(
            model=GroundingDINO._static_model,
            image=rgbimage_tensor,
            caption=text_prompt,
            box_threshold=self.BOX_TRESHOLD,
            text_threshold=self.TEXT_TRESHOLD,
            device="cuda" if torch.cuda.is_available() else "cpu",
        )
        annotated_frame = annotate(rgbimage, boxes, logits, phrases)
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        if self.logging:
            rr.log_image("gdino/detection", annotated_frame)
            rr.log_annotation_context(
                "gdino/detection_result",
                [
                    (0, phrases[i] + f" with prob: {logits[i].item():0.2f}")
                    for i in range(len(boxes))
                ],
            )
        self.frames += 1
        boxes = boxes * torch.Tensor([w, h, w, h])
        boxes = box_convert(boxes=boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()
        return boxes, phrases


if __name__ == "__main__":
    rr.init("gdino/turbine", spawn=True)
    # test groundingdino
    img_path = "./data/turbine2.png"
    # read image
    img = np.asarray(Image.open(img_path).convert("RGB"))
    rr.log_image("gdino/raw_image", img)
    gdinotool = GroundingDINO()
    text_prompt = "turbine"
    boxes, phrases = gdinotool.run(img, text_prompt)
