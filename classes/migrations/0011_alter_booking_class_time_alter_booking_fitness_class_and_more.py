# Generated by Django 5.0.7 on 2025-02-03 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0010_alter_booking_class_time_alter_classtime_time_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='class_time',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='fitness_class',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='visitor_phone',
            field=models.CharField(max_length=50),
        ),
    ]
