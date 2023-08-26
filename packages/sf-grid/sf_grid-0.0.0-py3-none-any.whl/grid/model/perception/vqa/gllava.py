import os
import numpy as np
import torch

from llava.constants import (
    IMAGE_TOKEN_INDEX,
    DEFAULT_IMAGE_TOKEN,
    DEFAULT_IM_START_TOKEN,
    DEFAULT_IM_END_TOKEN,
)
from llava.conversation import conv_templates, SeparatorStyle
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from llava.mm_utils import (
    tokenizer_image_token,
    get_model_name_from_path,
    KeywordsStoppingCriteria,
)


from grid.model.model import Model, modelregistry


@modelregistry.register_model(name="vqa-llava")
class GLLaVA:
    """visual question answering model based on LLaVA."""

    _static_model = None
    _static_tokenizer = None
    _static_image_processor = None
    _static_context_len = None

    # ref: https://github.com/haotian-liu/LLaVA/blob/main/llava/eval/run_llava.py
    def __init__(self) -> None:
        assert torch.cuda.is_available(), "LLaVA requires a GPU to run."
        disable_torch_init()
        super().__init__()

        if GLLaVA._static_model is None:
            from grid import GRIDConfig

            model_weights_dir = os.path.join(
                GRIDConfig().get_main_dir(),
                "external",
                "model_weights",
                "LLaVA",
                "LLaVA-Lightning-7B-v1-1",
                "",  # make sure model_weights_dir ends with a slash so that transformer reads locally
            )
            model_name = get_model_name_from_path(model_weights_dir)
            (
                GLLaVA._static_tokenizer,
                GLLaVA._static_model,
                GLLaVA._static_image_processor,
                GLLaVA._static_context_len,
            ) = load_pretrained_model(
                model_weights_dir,
                None,
                model_name,
                False,
                False,
            )
            conv_mode = "llava_v1"
            self.msg_prefix = None
            if GLLaVA._static_model.config.mm_use_im_start_end:
                self.msg_prefix = (
                    DEFAULT_IM_START_TOKEN
                    + DEFAULT_IMAGE_TOKEN
                    + DEFAULT_IM_END_TOKEN
                    + "\n"
                )
            else:
                self.msg_prefix = DEFAULT_IMAGE_TOKEN + "\n"

        self.conversation_template = conv_templates[conv_mode]

        # print("roles", self.conv_template.roles)
        # users, assistant

    def run(self, image: np.ndarray, instruction: str) -> str:
        """respond to the instruction given the image.

        Args:
            image (np.ndarray): the image we are interested in
            instruction (str): task instruction

        Returns:
            str: response following the instruction and the image
        """
        image_tensor = (
            GLLaVA._static_image_processor.preprocess(image, return_tensors="pt")[
                "pixel_values"
            ]
            .half()
            .cuda()
        )

        instruction = self.msg_prefix + instruction
        conversation = self.conversation_template.copy()
        conversation.append_message(conversation.roles[0], instruction)
        # not sure what this does
        # conversation.append_message(conversation.roles[1], None)
        prompt = conversation.get_prompt()
        input_ids = (
            tokenizer_image_token(
                prompt, GLLaVA._static_tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt"
            )
            .unsqueeze(0)
            .cuda()
        )
        stop_str = (
            conversation.sep
            if conversation.sep_style != SeparatorStyle.TWO
            else conversation.sep2
        )
        keywords = [stop_str]
        stopping_criteria = KeywordsStoppingCriteria(
            keywords, GLLaVA._static_tokenizer, input_ids
        )
        with torch.inference_mode():
            output_ids = GLLaVA._static_model.generate(
                input_ids,
                images=image_tensor.unsqueeze(0).half().cuda(),
                do_sample=True,
                temperature=0.2,
                max_new_tokens=1024,
                use_cache=True,
                stopping_criteria=[stopping_criteria],
            )

        answer = (
            GLLaVA._static_tokenizer.decode(output_ids[0, input_ids.shape[1] :])
            .strip()
            .rstrip(stop_str)
        )
        return answer


if __name__ == "__main__":
    from PIL import Image

    img_path = "./data/image/fire.png"
    img = np.asarray(Image.open(img_path).convert("RGB"))
    llava = GLLaVA()
    outputs = llava.run(img, "describe the image.")
    print("answers")
    print(outputs)
    print("done")
