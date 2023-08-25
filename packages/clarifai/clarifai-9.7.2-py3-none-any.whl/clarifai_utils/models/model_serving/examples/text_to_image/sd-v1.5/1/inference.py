# This file contains boilerplate code to allow users write their model
# inference code that will then interact with the Triton Inference Server
# Python backend to serve end user requests.
# The module name, module path, class name & get_predictions() method names MUST be maintained as is
# but other methods may be added within the class as deemed fit provided
# they are invoked within the main get_predictions() inference method
# if they play a role in any step of model inference
"""User model inference script."""

import os
from pathlib import Path

import numpy as np
import torch
from diffusers import StableDiffusionPipeline

from clarifai.models.model_serving.models.model_types import text_to_image
from clarifai.models.model_serving.models.output import ImageOutput


class InferenceModel:
  """User model inference class."""

  def __init__(self) -> None:
    """
    Load inference time artifacts that are called frequently .e.g. models, tokenizers, etc.
    in this method so they are loaded only once for faster inference.
    """
    self.base_path: Path = os.path.dirname(__file__)
    self.huggingface_model_path = os.path.join(self.base_path, "stable-diffusion-v1-5")
    self.device = "cuda" if torch.cuda.is_available() else "cpu"
    self.pipeline = StableDiffusionPipeline.from_pretrained(
        self.huggingface_model_path, torch_dtype=torch.float16)
    self.pipeline = self.pipeline.to(self.device)

  @text_to_image
  def get_predictions(self, input_data):
    """
    Main model inference method.

    Args:
    -----
      input_data: A single input data item to predict on.
        Input data can be an image or text, etc depending on the model type.

    Returns:
    --------
      One of the clarifai.models.model_serving.models.output types. Refer to the README/docs
    """
    out_image = self.pipeline(input_data).images[0]
    out_image = np.asarray(out_image)
    return ImageOutput(image=out_image)
