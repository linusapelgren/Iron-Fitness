# Generated by Django 5.0.7 on 2024-07-26 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_userprofile_subscription_duration_months'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='subscription_duration_months',
        ),
    ]
