import numpy as np
import torch
from transformers import DPTForDepthEstimation, DPTImageProcessor
from grid.model.model import Model, modelregistry


@modelregistry.register_model(name="depth-midas")
class MIDAS(Model):
    def __init__(self) -> None:
        self.model = DPTForDepthEstimation.from_pretrained(
            f"Intel/dpt-hybrid-midas", low_cpu_mem_usage=True
        )
        self.feature_extractor = DPTImageProcessor.from_pretrained(
            f"Intel/dpt-hybrid-midas"
        )

        if torch.cuda.is_available():
            self.device = "cuda:0"
            self.model.to(self.device)
        else:
            self.device = "cpu"

    def run(self, rgbimage: np.ndarray) -> np.ndarray:
        inputs = self.feature_extractor(images=rgbimage, return_tensors="pt")
        inputs = inputs.to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            predicted_depth = outputs.predicted_depth

        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=rgbimage.shape[:2],
            mode="bicubic",
            align_corners=False,
        )
        output = prediction.squeeze().cpu().numpy()
        return output


if __name__ == "__main__":
    from PIL import Image
    import cv2

    img_path = "./data/image/fire4depth.png"
    img = np.asarray(Image.open(img_path).convert("RGB"))
    midas = MIDAS()
    depth = midas.run(img)
    formatted = (depth * 255 / np.max(depth)).astype("uint8")
    depth = Image.fromarray(formatted)
    depth.show()
