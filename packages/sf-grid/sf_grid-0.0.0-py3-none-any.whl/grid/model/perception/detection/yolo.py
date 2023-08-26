from typing import List
import os
import numpy as np
from ultralytics.models import YOLO
from ultralytics.engine.results import Results

from grid.model.model import Model, modelregistry


@modelregistry.register_model(name="detection-yolo")
class Yolo(Model):
    """Object detection models for rgb images based on yolov8.

    Args:
        Tool (_type_): _description_
    """

    # add 'the fire may not appear in your first scan of rgb image``

    def __init__(self) -> None:
        """Initialize yolo detection model."""
        from grid import GRIDConfig

        super().__init__()
        self._model = YOLO(
            os.path.join(GRIDConfig.get_main_dir(), "external", "yolov8x.pt")
        )

    def run(self, rgbimage: np.ndarray) -> List[Results]:
        """Given a rgb image represented by np.ndarray, run yolo detection over the image. Retrun a
        list of results.

        Args:
            rgbimage (np.ndarray): _description_

        Returns:
            List[Results]: A list of yolov8 detect results.

        Example usage of results returned by this function:
            >>> for result in results:
            >>>     porbs = results[0].probs  # cls prob, (num_class, )
            >>>     masks = results[0].masks  # Masks object
            >>>     masks.xy  # x, y segments (pixels), List[segment] * N
            >>>     masks.xyn  # x, y segments (normalized), List[segment] * N
            >>>     masks.data  # raw masks tensor, (N, H, W) or masks.masks
            >>>     boxes = result.boxes # object detect boxes
            >>>     for box in boxes:
            >>>         box.xyxy  # box with xyxy format, (N, 4)
            >>>         box.xywh  # box with xywh format, (N, 4)
            >>>         box.xyxyn  # box with xyxy format but normalized, (N, 4)
            >>>         box.xywhn  # box with xywh format but normalized, (N, 4)
            >>>         box.conf  # confidence score, (N, 1)
            >>>         box.cls  # cls, (N, 1)
            >>>         self.cls2Name(box.cls)  # cls name
            >>>         boxes.data  # raw bboxes tensor, (N, 6) or boxes.box
        """
        results = self._model.predict(
            source=rgbimage,  # save=True, save_txt=True
        )  # save predictions as labels

        return results

    def cls2Name(self, cls: np.ndarray) -> str:
        """Return the class name given the class id of box.

        Args:
            cls (np.ndarray): class values of the boxes

        Returns:
            str: class names of the boxes
        """
        return self._model.names[int(cls)]


if __name__ == "__main__":
    from PIL import Image

    # test yolo
    img_path = "./data/airsim_forest.png"
    # readm image
    img = np.array(Image.open(img_path).convert("RGB"))
    yolo = Yolo()
    results = yolo.run(img)
    # for result in results:
    #    print(result.xyxy[0])
