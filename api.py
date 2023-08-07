import requests
from PIL import Image
from io import BytesIO
from config import Config

url = "https://dezgo.p.rapidapi.com/text2image"

# set general parameters of request, prompt should be replaced
payload = {
    "prompt": "",
    "guidance": "7",
    "steps": "30",
    "sampler": "euler_a",
    "upscale": "1",
    "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft",
    "model": "epic_diffusion_1_1",
}
headers = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Key": Config.API_KEY,
    "X-RapidAPI-Host": "dezgo.p.rapidapi.com",
}


def generate(prompt):
    payload["prompt"] = prompt
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        return

    # Check if the request was successful
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))  # construct PIL Image from content
        return image
