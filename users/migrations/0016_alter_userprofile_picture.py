# Generated by Django 5.0.7 on 2024-07-24 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0015_alter_userprofile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="picture",
            field=models.ImageField(
                default="profile_pics/blank_profile.png", upload_to="profile_pics/"
            ),
        ),
    ]
