import os
from flask import current_app
from PIL import Image

color_list = [
    "red",
    "blue",
    "black_and_white",
    "black",
    "white",
    "yellow",
    "orange",
    "purple",
    "magenta",
    "green",
    "teal",
]

orientation_list = ["landscape", "portrait", "squarish"]


class ImageSaveError(Exception):
    pass


def thumb_image(image_name: str):
    im = Image.open(image_name)
    im.thumbnail((200, 200))
    im.save(image_name)


def save_image(img_name: str, img_content: bytes):
    try:
        with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                current_app.config["STATIC_FOLDER"],
                img_name,
            ),
            "wb",
        ) as f:
            f.write(img_content)
        img_path = os.path.join(current_app.config["STATIC_FOLDER"], img_name)
        thumb_image(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_path))
    except (OSError, IOError, Exception):
        raise ImageSaveError


def create_query(search_param: str, data: str) -> dict:
    query = None
    try:
        query = {"query": {f"{search_param.lower()}:{data}"}}
    except (KeyError, AttributeError):
        pass
    return query


def is_image(content_type: str) -> bool:
    if content_type.lower() in ["image/jpg", "image/jpeg", "image/png"]:
        return True
    return False


def validate_query(query_string: dict) -> (bool, dict):
    payload = {}
    valid = False
    if query_string:
        if len(query_string.keys()) > 1:
            payload = {
                "message": "Please use either color or orientation as a search parameter"
            }
        for k, v in query_string.items():
            if not (k == "color" or k == "orientation"):
                payload = {
                    "message": "Please use either color or orientation as a search parameter"
                }
                break
            if k == "color" and (v not in color_list and not v == ""):
                payload = {
                    "message": f"Please use on of {color_list} for your color selection"
                }
                break
            elif k == "orientation" and (v not in orientation_list and not v == ""):
                payload = {
                    "message": f"Please use on of {orientation_list} for your orientation selection"
                }
                break
            else:
                valid = True
        return valid, payload
    return True, {}
