import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URL = os.environ.get("DB_URL")
    API_KEY = os.environ.get("API_KEY")
    IMAGES_DIR = os.environ.get("IMAGES_DIR")
