# Import libraries
import cv2
import io
import cvlib as cv
import numpy as np
from PIL import Image
from cvlib.object_detection import draw_bbox


# reading by each frame
def detect(file_django):
    image_bytesio = io.BytesIO(file_django.read())
    image_bytes = image_bytesio.getvalue()
    image_nparray = np.fromstring(image_bytes, np.uint8)
    image_np = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
    bbox, label, conf = cv.detect_common_objects(image_np)  # find all common objects in frame
    image_np_output = draw_bbox(image_np, bbox, label, conf)  # draw box above object
    width, height, channels = image_np.shape
    image_np_outout_rgb = cv2.cvtColor(image_np_output, cv2.COLOR_BGR2RGB)
    image_output = Image.fromarray(image_np_outout_rgb)
    return image_to_byte_array(image_output), height, width


def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
