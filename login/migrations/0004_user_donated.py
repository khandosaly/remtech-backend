# Generated by Django 3.2.3 on 2021-05-27 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20210527_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='donated',
            field=models.IntegerField(default=0),
        ),
    ]