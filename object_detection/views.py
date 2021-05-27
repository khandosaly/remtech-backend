import base64
import os

import cv2
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import object_detection.opencv as cv
from login.models import User
from remtech_django import settings


@csrf_exempt
def index(request):
    if request.method == "POST":
        username = request.body.decode('cp437').split('username"')[1].split('-')[0].split()[0]
        if 'object_detection' in request.FILES:
            if username != 'anonym':
                usr = User.objects.get(nick=username)
                usr.count_detect += 1
                usr.save()
            file_django = request.FILES['object_detection']
            image_pil, w, h, image_to_save = cv.detect(file_django, username)
            image_b64 = base64.b64encode(image_pil).decode('utf-8')
            ctx = {'image': image_b64, 'w': w, 'h': h}
            return JsonResponse(ctx, safe=False)
