import base64

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import object_detection.opencv as cv


@csrf_exempt
def index(request):
    if request.method == "POST":
        if 'object_detection' in request.FILES:
            file_django = request.FILES['object_detection']
            image_pil, w, h = cv.detect(file_django)
            image_b64 = base64.b64encode(image_pil).decode('utf-8')
            ctx = {'image': image_b64, 'w': w, 'h': h}
            return JsonResponse(ctx, safe=False)