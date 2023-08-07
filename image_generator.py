import os
import matplotlib

matplotlib.use("TkAgg")  # user tkinter backend to display things

import matplotlib.pyplot as plt
from PIL.Image import Image as PLTImage
from PIL import Image
import numpy as np

import utils
from api import generate
from config import Config
from db import create_db_tables, PromptHistory, get_db_session


class ImageGenerator:
    def __init__(self):
        # make sure that images folder and tables are created and ready for future use
        create_db_tables()
        if not os.path.exists(Config.IMAGES_DIR):
            os.makedirs(Config.IMAGES_DIR)

    def generate_image(self, prompt, save_to_db=True):
        image = generate(prompt)
        if save_to_db:
            self.save_data(prompt, image)
        self.display_image(image)

    def save_data(self, prompt: str, image: PLTImage):
        image_name = utils.generate_random_image_name(extension=".png")
        image_path = f"{Config.IMAGES_DIR}/{image_name}"
        image.save(image_path)

        prompt_record = PromptHistory(prompt=prompt, image_path=image_path)
        with get_db_session() as db_session:
            prompt_record.save_to_db(db_session=db_session)

    def display_image(self, image: PLTImage):
        img_array = np.array(image)
        plt.imshow(img_array)
        plt.axis("off")  # Hide axes
        plt.show()

    def display_image_with_path(self, image_path):
        image = Image.open(image_path)
        self.display_image(image)

    def display_image_with_prompt_id(self, prompt_id):
        image_path = None
        with get_db_session() as db_session:
            prompt = PromptHistory.find_by_id(
                prompt_id=prompt_id, db_session=db_session
            )
            if prompt:
                image_path = prompt.image_path
        if image_path is None:
            print("such record does not exist")
            return
        self.display_image_with_path(image_path)

    def get_prompt_history(self):
        with get_db_session() as db_session:
            prompt_records = PromptHistory.get_all(db_session=db_session)

            template = "{:>4}: {}"
            return (
                template.format("(id)", "(prompt)")
                + "\n--------------\n"
                + "\n".join(
                    template.format(prompt.id, prompt.prompt)
                    for prompt in prompt_records
                )
            )

    def clear_history(self):
        with get_db_session() as db_session:
            PromptHistory.remove_all(db_session=db_session)
        utils.remove_files_from_directory(Config.IMAGES_DIR)


if __name__ == "__main__":
    image_generator = ImageGenerator()

    image_generator.generate_image(
        "an astronaut riding a horse, digital art, epic lighting, highly-detailed masterpiece trending HQ"
    )

    print(image_generator.get_prompt_history())
