import encrypted_fields.fields
from django.db import models


class User(models.Model):
    nick = models.TextField()
    email = models.EmailField()
    password = encrypted_fields.fields.EncryptedCharField(max_length=40)
