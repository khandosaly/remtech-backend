import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from login.models import User


@csrf_exempt
def index(request):
    if request.method == "POST":
        data = request.body.decode('utf-8')
        data = json.loads(data)
        if 'email' in data.keys():
            if User.objects.filter(nick=data['nick']).exists():
                ans = {'STATE': 'Username is already in use.'}
            elif User.objects.filter(email=data['email']).exists():
                ans = {'STATE': 'Email is already in use.'}
            else:
                usr = User(nick=data['nick'], email=data['email'], password=data['pass'])
                usr.save()
                ans = {'STATE': 'Success!'}
            return JsonResponse(ans)
        else:
            if User.objects.filter(nick=data['nick']).exists():
                u = User.objects.get(nick=data['nick'])
                if u.password == data['pass']:
                    ans = {'STATE': 'Success!'}
                else:
                    ans = {'STATE': 'Invalid username or password'}
            else:
                ans = {'STATE': 'Invalid username or password'}
            return JsonResponse(ans)
