# Import libraries
import io
import cv2
import numpy as np
from PIL import Image

from face_swap.face_detection import select_face
from face_swap.face_swap import face_swap


# reading by each frame
from login.models import User


def swap(file_django_src, file_django_dst, username):
    image_bytesio_src = io.BytesIO(file_django_src.read())
    image_bytes_src = image_bytesio_src.getvalue()
    image_nparray_src = np.fromstring(image_bytes_src, np.uint8)
    src_img = cv2.imdecode(image_nparray_src, cv2.IMREAD_COLOR)

    image_bytesio_dst = io.BytesIO(file_django_dst.read())
    image_bytes_dst = image_bytesio_dst.getvalue()
    image_nparray_dst = np.fromstring(image_bytes_dst, np.uint8)
    dst_img = cv2.imdecode(image_nparray_dst, cv2.IMREAD_COLOR)

    src_points, src_shape, src_face = select_face(src_img)
    dst_points, dst_shape, dst_face = select_face(dst_img)
    output = face_swap(src_face, dst_face, src_points, dst_points, dst_shape, dst_img)

    width, height, channels = output.shape
    image_np_output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    image_output = Image.fromarray(image_np_output_rgb)
    if username != 'anonym':
        cv2.imwrite(f'/home/khandosaly/remtech/back/media/{username}_face_swap.jpg', output)
        usr = User.objects.get(nick=username)
        usr.photo_face_swap = f'/home/khandosaly/remtech/back/media/{username}_face_swap.jpg'
        usr.save()
    return image_to_byte_array(image_output), height, width, image_np_output_rgb


def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
