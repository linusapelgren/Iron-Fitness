# Generated by Django 5.0.7 on 2024-07-26 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_userprofile_stripe_subscription_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='stripe_subscription_id',
        ),
    ]