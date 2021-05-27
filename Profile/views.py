import base64
import io
import json
import cv2
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from login.models import *


@csrf_exempt
def index(request):
    data = json.loads(request.body.decode('utf-8'))
    usr = User.objects.get(nick=data['username'])
    ctx = {'STATE': 'Success!', 'count_detect': usr.count_detect, 'count_pointillism': usr.count_pointillism,
           'count_face_swap': usr.count_face_swap, 'donated': usr.donated}
    try:
        if len(usr.photo_detect) > 0:
            img_detect = image_to_byte_array(Image.open(str(usr.photo_detect)))
            ctx['detect'] = base64.b64encode(img_detect).decode('utf-8')
    except ValueError:
        ctx['detect'] = 'None'
    try:
        if len(usr.photo_pointillism) > 0:
            img_pointillism = image_to_byte_array(Image.open(str(usr.photo_pointillism)))
            ctx['pointillism'] = base64.b64encode(img_pointillism).decode('utf-8')
    except ValueError:
        ctx['pointillism'] = 'None'
    try:
        if len(usr.photo_face_swap) > 0:
            img_face_swap = image_to_byte_array(Image.open(str(usr.photo_face_swap)))
            ctx['face_swap'] = base64.b64encode(img_face_swap).decode('utf-8')
    except ValueError:
        ctx['face_swap'] = 'None'
    return JsonResponse(ctx, safe=False)


@csrf_exempt
def donate(request):
    data = json.loads(request.body.decode('utf-8'))
    ctx = {'STATUS': 'OK'}
    if data['username'] != 'anonym':
        usr = User.objects.get(nick=data['username'])
        usr.donated += int(data['amount'])
        usr.save()
    return JsonResponse(ctx, safe=False)


def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
