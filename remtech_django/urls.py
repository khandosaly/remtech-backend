from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import Profile.views
import face_swap.views
import login.views
import object_detection.views
import pointillism.views
from remtech_django import settings

urlpatterns = [
    path('object_detection/', object_detection.views.index),
    path('pointillism/', pointillism.views.index),
    path('face_swap/', face_swap.views.index),
    path('login/', login.views.login),
    path('admin/', admin.site.urls),
    path('profile/', Profile.views.index),
    path('donate/', Profile.views.donate)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
