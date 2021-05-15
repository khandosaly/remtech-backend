import base64

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import opencv as cv


@csrf_exempt
def index(request):
    if request.method == "POST":
        if 'pointillism' in request.FILES:
            file_django = request.FILES['pointillism']
            image_pil, w, h = cv.pointillist(file_django)
            image_b64 = base64.b64encode(image_pil).decode('utf-8')
            ctx = {'image': image_b64, 'w': w, 'h': h}
            return JsonResponse(ctx, safe=False)