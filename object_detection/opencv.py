# Import libraries
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

import numpy as np

import cv2
import math
import progressbar
from . import color_palette
from . import utils
from . import vector_field


# reading by each frame
def detect(path):
    frame = cv2.imread(f'{path}')
    bbox, label, conf = cv.detect_common_objects(frame)  # find all common objects in frame
    output_image = draw_bbox(frame, bbox, label, conf)  # draw box above object
    cv2.imwrite(f'{path}-edited.jpg', output_image)
    width, height, channels = frame.shape
    return height, width


def pointillist(img_path):
    palette_size = 20
    stroke_scale = 0
    gradient_smoothing_radius = 0
    limit_image_size = 0
    res_path = img_path + "-edited.jpg"
    img = cv2.imread(img_path)
    width, height, channels = img.shape
    if limit_image_size > 0:
        img = utils.limit_size(img, limit_image_size)
    if stroke_scale == 0:
        stroke_scale = int(math.ceil(max(img.shape) / 1000))
    else:
        stroke_scale = stroke_scale
    if gradient_smoothing_radius == 0:
        gradient_smoothing_radius = int(round(max(img.shape) / 50))
    else:
        gradient_smoothing_radius = gradient_smoothing_radius
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    palette = color_palette.ColorPalette.from_image(img, palette_size)
    palette = palette.extend([(0, 50, 0), (15, 30, 0), (-15, 30, 0)])
    gradient = vector_field.VectorField.from_gradient(gray)
    gradient.smooth(gradient_smoothing_radius)
    res = cv2.medianBlur(img, 11)
    grid = utils.randomized_grid(img.shape[0], img.shape[1], scale=3)
    batch_size = 10000
    bar = progressbar.ProgressBar()
    for h in bar(range(0, len(grid), batch_size)):
        pixels = np.array([img[x[0], x[1]] for x in grid[h:min(h + batch_size, len(grid))]])
        color_probabilities = utils.compute_color_probabilities(pixels, palette, k=9)
        for i, (y, x) in enumerate(grid[h:min(h + batch_size, len(grid))]):
            color = utils.color_select(color_probabilities[i], palette)
            angle = math.degrees(gradient.direction(y, x)) + 90
            length = int(round(stroke_scale + stroke_scale * math.sqrt(gradient.magnitude(y, x))))
            cv2.ellipse(res, (x, y), (length, stroke_scale), angle, 0, 360, color, -1, cv2.LINE_AA)
    cv2.imwrite(res_path, res)
    return height, width
