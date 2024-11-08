# Generated by Django 4.2.5 on 2023-11-27 07:00

import django.utils.timezone
from django.db import migrations, models
from django.db.models import F


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0402_patientconsultation_new_discharge_reason"),
    ]

    def clean_encounter_date(apps, schema_editor):
        PatientConsultation = apps.get_model("facility", "PatientConsultation")

        # Set `encounter_date` to `created_date` for all consultations with
        # suggestions that are not Admission, Domiciliary Care.
        #
        # Reason:
        # We were not capturing `admission_date` (now `encounter_date`) for
        # these consultations earlier, but could still be set by mistake.
        #
        # Example:
        # Edit Consultation allowed changing suggestion to non Admission/Domiciliary Care
        # without clearing `admission_date` (now `encounter_date`).
        PatientConsultation.objects.exclude(suggestion__in=["A", "DC"]).update(
            encounter_date=F("created_date")
        )

        # Set `encounter_date` to `created_date` for all consultations with
        # `encounter_date` as `null`.
        #
        # Reason:
        # We were not capturing `encounter_date` for these consultations as
        # it was not set for these.
        PatientConsultation.objects.filter(encounter_date=None).update(
            encounter_date=F("created_date")
        )

    def reverse_clean_encounter_date(apps, schema_editor):
        PatientConsultation = apps.get_model("facility", "PatientConsultation")

        # Set `encounter_date` to `null` for all consultations with suggestions
        # that are not Admission/Domiciliary Care.
        PatientConsultation.objects.exclude(suggestion__in=["A", "DC"]).update(
            encounter_date=None
        )

    operations = [
        migrations.RemoveConstraint(
            model_name="patientconsultation",
            name="if_admitted",
        ),
        migrations.RenameField(
            model_name="patientconsultation",
            old_name="admission_date",
            new_name="encounter_date",
        ),
        migrations.RunPython(
            clean_encounter_date,
            reverse_code=reverse_clean_encounter_date,
        ),
        migrations.AlterField(
            model_name="patientconsultation",
            name="encounter_date",
            field=models.DateTimeField(
                db_index=True, default=django.utils.timezone.now
            ),
        ),
    ]
