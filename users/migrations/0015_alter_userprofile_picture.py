# Generated by Django 5.0.7 on 2024-07-22 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_userprofile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default='{% static blank_profile/blank_profile.png %}', upload_to='{% static profile_pics/ %}'),
        ),
    ]