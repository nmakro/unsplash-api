from PIL import Image


def thumb_image(image_name):
    im = Image.open(image_name)
    im.thumbnail((200, 200))
    im.save(image_name)
