import base64

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import face_swap.opencv as cv
from login.models import User


@csrf_exempt
def index(request):
    if request.method == "POST":
        username = request.body.decode('cp437').split('username"')[1].split('-')[0].split()[0]
        if 'face_swap_src' in request.FILES and 'face_swap_dst' in request.FILES:
            if username != 'anonym':
                usr = User.objects.get(nick=username)
                usr.count_face_swap += 1
                usr.save()
            file_django_src = request.FILES['face_swap_src']
            file_django_dst = request.FILES['face_swap_dst']
            image_pil, w, h, image_to_save = cv.swap(file_django_src, file_django_dst, username)
            image_b64 = base64.b64encode(image_pil).decode('utf-8')
            ctx = {'image': image_b64, 'w': w, 'h': h}
            return JsonResponse(ctx, safe=False)
