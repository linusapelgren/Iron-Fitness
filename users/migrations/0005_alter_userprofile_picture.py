# Generated by Django 5.0.7 on 2024-07-19 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_userprofile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="picture",
            field=models.ImageField(
                default="blank_profile.png", upload_to="profile_pics/"
            ),
        ),
    ]
