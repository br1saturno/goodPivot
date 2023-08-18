import os
import requests
import base64
import random


def sd_generation(prompt, folder, image_word,  samples, style=None):
    """ Prompt, folder where the image will be saved in the static directory, word that will identify the series of
    images, number of samples, style preset (optional): 3d-model analog-film anime cinematic comic-book digital-art
    enhance fantasy-art isometric line-art low-poly modeling-compound neon-punk origami photographic pixel-art
    tile-texture  """

    engine_id = "stable-diffusion-xl-beta-v2-2-2"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = os.getenv("STABILITY_KEY")

    if api_key is None:
        raise Exception("Missing Stability API key.")

    image_prompt = prompt

    negatives = "Disfigured, Deformed, Low quality, Watermark, Signature, Logo, Bad anatomy, Extra hands, Extra arms, Extra legs, Extra fingers, Mutation, Mutilated, Missing fingers, Low resolution"

    answers = requests.post(f"{api_host}/v1/generation/{engine_id}/text-to-image", headers={
        "Content-Type": "application/json", "Accept": "application/json", "Authorization": f"Bearer {api_key}"}, json={
        "text_prompts": [ {"text": f'{str(image_prompt)}', "weight": 1},
            {"text": f'{str(negatives)}', "weight": -1.5}, ], "cfg_scale": 5, "clip_guidance_preset": "FAST_BLUE",
        "samples": samples, "steps": 50,  "style_preset": style,  # "seed": 6783409245865679,
    }, )

    data = answers.json()

    image_base_url = f"./apps/home/static/{folder}/"
    image_list = [ ]
    for i, image in enumerate(data[ "artifacts" ]):
        image_code = random.randint(1000, 99999)
        with open(f"{image_base_url}{image_word}_{image_code}_{i}.png", "wb") as f:
            f.write(base64.b64decode(image[ "base64" ]))
        image_list.append(f"/assets/{folder}/{image_word}_{image_code}_{i}.png")

    if answers.status_code != 200:
        msg = "Sorry, we're experiencing high demand at the moment. Please try again."
        status = "invalid"
        print(Exception("Non-200 response: " + str(answers.text)))
        return msg, status

    return image_list
