import PIL.ImageEnhance
from PIL import Image

# Тут расположены эффекты для фоток

def brightness(img: Image.Image, parm: int) -> Image.Image:
    img = PIL.ImageEnhance.Brightness(img).enhance(parm)
    return img

def color(img: Image.Image, parm: int) -> Image.Image:
    img = PIL.ImageEnhance.Color(img).enhance(parm)
    return img

def contrast(img: Image.Image, parm: int) -> Image.Image:
    img = PIL.ImageEnhance.Contrast(img).enhance(parm)
    return img

def sharpness(img: Image.Image, parm: int) -> Image.Image:
    img = PIL.ImageEnhance.Sharpness(img).enhance(parm)
    return img

def rotate(img: Image.Image, parm: int) -> Image.Image:
    img = img.rotate(parm, expand=True)
    return img



