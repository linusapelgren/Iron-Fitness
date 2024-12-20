# Generated by Django 5.0.7 on 2024-07-20 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_userprofile_address"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userprofile",
            old_name="address",
            new_name="street_address",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="postal_code",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="state",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
