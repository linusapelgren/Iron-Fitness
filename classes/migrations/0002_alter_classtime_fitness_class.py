# Generated by Django 5.0.7 on 2024-07-24 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classtime',
            name='fitness_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_times', to='classes.fitnessclass'),
        ),
    ]
