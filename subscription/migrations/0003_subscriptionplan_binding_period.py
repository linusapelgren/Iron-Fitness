# Generated by Django 5.0.7 on 2024-07-26 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscription", "0002_alter_subscriptionplan_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptionplan",
            name="binding_period",
            field=models.IntegerField(default=0),
        ),
    ]
