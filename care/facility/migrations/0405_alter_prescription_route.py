# Generated by Django 4.2.5 on 2024-01-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0404_merge_20231220_2227"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prescription",
            name="route",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ORAL", "Oral"),
                    ("IV", "IV"),
                    ("IM", "IM"),
                    ("SC", "S/C"),
                    ("INHALATION", "Inhalation"),
                    ("NASOGASTRIC", "Nasogastric/Gastrostomy tube"),
                    ("INTRATHECAL", "intrathecal injection"),
                    ("TRANSDERMAL", "Transdermal"),
                    ("RECTAL", "Rectal"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]
