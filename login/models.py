import encrypted_fields.fields
from django.db import models


class User(models.Model):
    nick = models.TextField()
    email = models.EmailField()
    password = encrypted_fields.fields.EncryptedCharField(max_length=40)
    photo_detect = models.ImageField(null=True, upload_to='images')
    photo_face_swap = models.ImageField(null=True, upload_to='images')
    photo_pointillism = models.ImageField(null=True, upload_to='images')
    count_detect = models.IntegerField(default=0)
    count_face_swap = models.IntegerField(default=0)
    count_pointillism = models.IntegerField(default=0)
    donated = models.IntegerField(default=0)
