# Generated by Django 3.2.3 on 2021-05-27 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20210525_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='count_detect',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='count_face_swap',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='count_pointillism',
            field=models.IntegerField(default=0),
        ),
    ]
