# Generated by Django 4.2.4 on 2023-09-01 16:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_alter_user_profile_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_img",
            field=models.CharField(blank=True, null=True),
        ),
    ]