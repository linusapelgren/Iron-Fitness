# Generated by Django 5.0.7 on 2024-07-19 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_userprofile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default='blank_profile.png', upload_to='media/profile_pics/'),
        ),
    ]
