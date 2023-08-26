import numpy as np
import torch
from transformers import AutoImageProcessor, DeformableDetrForObjectDetection

from grid.model.model import Model, modelregistry


@modelregistry.register_model(name="detection-detic_detr")
class DeticDETR(Model):
    def __init__(self) -> None:
        self.processor = AutoImageProcessor.from_pretrained("facebook/deformable-detr-detic")
        self.model = DeformableDetrForObjectDetection.from_pretrained("facebook/deformable-detr-detic")

        if torch.cuda.is_available():
            self.device = "cuda:0"
            self.model.to(self.device)
        else:
            self.device = "cpu"

    def run(self, rgbimage: np.ndarray) -> np.ndarray:
        inputs = self.processor(images=rgbimage, return_tensors="pt")
        inputs = inputs.to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)

        target_sizes = torch.tensor([rgbimage.size[::-1]])
        results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.7)[0]

        # TODO @sai: return the results?
        return results
