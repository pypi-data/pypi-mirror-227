import numpy as np
import torch
from transformers import AutoProcessor, Blip2ForConditionalGeneration

from grid.model.model import Model, modelregistry


@modelregistry.register_model(name="captioning-blip")
class BLIPv2(Model):
    def __init__(self) -> None:
        self.processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-opt-2.7b", device_map="auto", load_in_8bit=True
        )

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def run(self, image: np.ndarray, question: str) -> str:
        question_processed = f"Question: {question} Answer: "
        inputs = self.processor(image, text=question_processed, return_tensors="pt").to(self.device, torch.float16)

        generated_ids = self.model.generate(**inputs, max_new_tokens=10)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        print(generated_text)
