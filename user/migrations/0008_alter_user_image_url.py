# Generated by Django 4.2.4 on 2023-09-02 22:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0007_alter_user_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="image_url",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]