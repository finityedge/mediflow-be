# Generated by Django 2.2.11 on 2020-03-20 18:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0008_auto_20200320_1847"),
    ]

    operations = [
        migrations.RenameField(
            model_name="facilitycapacity",
            old_name="capacity",
            new_name="current_capacity",
        ),
        migrations.AddField(
            model_name="facilitycapacity",
            name="total_capacity",
            field=models.IntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
    ]
