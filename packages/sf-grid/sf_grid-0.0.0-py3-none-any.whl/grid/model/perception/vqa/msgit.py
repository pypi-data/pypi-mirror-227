import numpy as np
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoProcessor,
    BlipForQuestionAnswering,
    ViltForQuestionAnswering,
)

from grid.model.model import Model, modelregistry


@modelregistry.register_model(name="vqa-git")
class GITBase(Model):
    def __init__(self) -> None:
        self.processor = AutoProcessor.from_pretrained("microsoft/git-base-vqav2")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-vqav2")

        self.device = "cpu"
        self.model.to(self.device)

    def run(self, image: np.ndarray, question: str) -> str:
        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values

        # prepare question
        input_ids = self.processor(text=question, add_special_tokens=False).input_ids
        input_ids = [self.processor.tokenizer.cls_token_id] + input_ids
        input_ids = torch.tensor(input_ids).unsqueeze(0)

        generated_ids = self.model.generate(
            pixel_values=pixel_values, input_ids=input_ids, max_length=50
        )
        generated_answer = self.processor.batch_decode(
            generated_ids, skip_special_tokens=True
        )

        return generated_answer
