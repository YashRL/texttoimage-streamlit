# -*- coding: utf-8 -*-
"""stable-diffusion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/woctezuma/stable-diffusion-colab/blob/main/stable_diffusion.ipynb
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install --quiet --upgrade diffusers transformers accelerate invisible_watermark mediapy

use_refiner = False

import mediapy as media
import random
import sys
import torch

from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
    )

if use_refiner:
  refiner = DiffusionPipeline.from_pretrained(
      "stabilityai/stable-diffusion-xl-refiner-1.0",
      text_encoder_2=pipe.text_encoder_2,
      vae=pipe.vae,
      torch_dtype=torch.float16,
      use_safetensors=True,
      variant="fp16",
  )

  refiner = refiner.to("cuda")

  pipe.enable_model_cpu_offload()
else:
  pipe = pipe.to("cuda")

prompt = "a photo of Pikachu fine dining with a view to the Eiffel Tower"
seed = random.randint(0, sys.maxsize)

negative_prompt = "3d, cartoon, anime, (deformed eyes, nose, ears, nose), bad anatomy, ugly"

images = pipe(
    prompt = prompt,
    negative_prompt = negative_prompt,
    output_type = "latent" if use_refiner else "pil",
    generator = torch.Generator("cuda").manual_seed(seed),
    ).images

if use_refiner:
  images = refiner(
      prompt = prompt,
      negative_prompt = negative_prompt,
      image = images,
      ).images

print(f"Prompt:\t{prompt}\nSeed:\t{seed}")
media.show_images(images)
images[0].save("output.jpg")