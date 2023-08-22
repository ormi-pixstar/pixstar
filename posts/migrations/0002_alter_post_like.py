# Generated by Django 4.2.4 on 2023-08-22 11:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='like_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
