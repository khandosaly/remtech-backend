import base64

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import face_swap.opencv as cv


@csrf_exempt
def index(request):
    if request.method == "POST":
        if 'face_swap_src' in request.FILES and 'face_swap_dst' in request.FILES:
            file_django_src = request.FILES['face_swap_src']
            file_django_dst = request.FILES['face_swap_dst']
            image_pil, w, h = cv.swap(file_django_src, file_django_dst)
            image_b64 = base64.b64encode(image_pil).decode('utf-8')
            ctx = {'image': image_b64, 'w': w, 'h': h}
            return JsonResponse(ctx, safe=False)
