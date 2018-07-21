import numpy as np
import PIL
from PIL import Image
import requests
from io import BytesIO

def mse(url_1, url_2):
    response_1 = requests.get(url_1)
    x = Image.open(
        BytesIO(response_1.content)
        ).resize(
        (32, 32), PIL.Image.ANTIALIAS
        ).convert('LA')
    x = np.array(x)
    response_2 = requests.get(url_2)
    y = Image.open(
        BytesIO(response_2.content)
        ).resize(
        (32, 32), PIL.Image.ANTIALIAS
        ).convert('LA')
    y = np.array(y)
    return np.linalg.norm(x - y)/100
