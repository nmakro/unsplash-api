from PIL import Image
from flask import current_app
import os


class ImageSaveError(Exception):
    pass


def thumb_image(image_name: str):
    im = Image.open(image_name)
    im.thumbnail((200, 200))
    im.save(image_name)


def save_image(img_name: str, img_content: bytes):
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), current_app.config["STATIC_FOLDER"], img_name), "wb") as f:
            f.write(img_content)
        img_path = os.path.join(current_app.config["STATIC_FOLDER"], img_name)
        thumb_image(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_path))
    except (OSError, IOError, Exception):
        raise ImageSaveError
