# Generated by Django 5.0.7 on 2024-07-26 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscription", "0004_remove_subscriptionplan_binding_period_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscriptionplan",
            name="binding_time",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
