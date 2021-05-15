# Import libraries
import io
import cv2
import math
import progressbar
import numpy as np
from PIL import Image

from . import color_palette
from . import utils
from . import vector_field


def pointillist(file_django):
    palette_size = 20
    stroke_scale = 0
    gradient_smoothing_radius = 0
    limit_image_size = 0
    image_bytesio = io.BytesIO(file_django.read())
    image_bytes = image_bytesio.getvalue()
    image_nparray = np.fromstring(image_bytes, np.uint8)
    image_np = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
    width, height, channels = image_np.shape
    if limit_image_size > 0:
        image_np = utils.limit_size(image_np, limit_image_size)
    if stroke_scale == 0:
        stroke_scale = int(math.ceil(max(image_np.shape) / 1000))
    else:
        stroke_scale = stroke_scale
    if gradient_smoothing_radius == 0:
        gradient_smoothing_radius = int(round(max(image_np.shape) / 50))
    else:
        gradient_smoothing_radius = gradient_smoothing_radius
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    palette = color_palette.ColorPalette.from_image(image_np, palette_size)
    palette = palette.extend([(0, 50, 0), (15, 30, 0), (-15, 30, 0)])
    gradient = vector_field.VectorField.from_gradient(gray)
    gradient.smooth(gradient_smoothing_radius)
    res = cv2.medianBlur(image_np, 11)
    grid = utils.randomized_grid(image_np.shape[0], image_np.shape[1], scale=3)
    batch_size = 10000
    bar = progressbar.ProgressBar()
    for h in bar(range(0, len(grid), batch_size)):
        pixels = np.array([image_np[x[0], x[1]] for x in grid[h:min(h + batch_size, len(grid))]])
        color_probabilities = utils.compute_color_probabilities(pixels, palette, k=9)
        for i, (y, x) in enumerate(grid[h:min(h + batch_size, len(grid))]):
            color = utils.color_select(color_probabilities[i], palette)
            angle = math.degrees(gradient.direction(y, x)) + 90
            length = int(round(stroke_scale + stroke_scale * math.sqrt(gradient.magnitude(y, x))))
            cv2.ellipse(res, (x, y), (length, stroke_scale), angle, 0, 360, color, -1, cv2.LINE_AA)
    img_rgb = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img_rgb)
    return image_to_byte_array(img), height, width


def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
