import base64

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from login.models import User
from . import opencv as cv


@csrf_exempt
def index(request):
    if request.method == "POST":
        username = request.body.decode('cp437').split('username"')[1].split('-')[0].split()[0]
        if 'pointillism' in request.FILES:
            if username != 'anonym':
                usr = User.objects.get(nick=username)
                usr.count_pointillism += 1
                usr.save()
            file_django = request.FILES['pointillism']
            image_pil, w, h, image_to_save = cv.pointillist(file_django, username)
            image_b64 = base64.b64encode(image_pil).decode('utf-8')
            ctx = {'image': image_b64, 'w': w, 'h': h}
            return JsonResponse(ctx, safe=False)