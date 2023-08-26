import numpy as np
import torch
import torchvision.transforms.functional as F
from transformers import CLIPSegForImageSegmentation, CLIPSegProcessor
import matplotlib.pyplot as plt
from grid.model.model import Model, modelregistry


@modelregistry.register_model(name="seg-clipseg")
class CLIPSeg(Model):
    def __init__(self) -> None:
        self.processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
        self.model = CLIPSegForImageSegmentation.from_pretrained(
            "CIDAS/clipseg-rd64-refined"
        )
        if torch.cuda.is_available():
            self.device = "cuda:0"
            self.model.to(self.device)
        else:
            self.device = "cpu"

    def run(self, rgbimage: np.ndarray, prompt: str) -> np.ndarray:
        """return segmentation heat map of rgb image

        Args:
            rgbimage (np.ndarray): _description_
            prompt (str): _description_

        Returns:
            np.ndarray: _description_
        """
        # rr.log_image("clipseg/input", rgbimage)
        inputs = self.processor(
            text=prompt, images=rgbimage, padding="max_length", return_tensors="pt"
        )
        inputs = inputs.to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            preds = torch.sigmoid(outputs.logits).cpu()
        preds = F.resize(
            preds.unsqueeze(0), (rgbimage.shape[0], rgbimage.shape[1]), antialias=True
        ).squeeze(0)
        # rr.log_segmentation_image("clipseg/seg", preds * 255)
        return (preds.numpy() * 255).astype(int)


if __name__ == "__main__":
    from PIL import Image
    import rerun as rr

    rr.init("clipseg", spawn=True)
    img_path = "rgbimage_turbine.png"
    img = np.asarray(Image.open(img_path).convert("RGB"))
    clipseg = CLIPSeg()
    seg = clipseg.run(img, "turbine")
