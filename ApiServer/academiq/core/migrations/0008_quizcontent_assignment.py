# Generated by Django 5.0.6 on 2024-06-05 14:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_grade_student"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizcontent",
            name="assignment",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.assignment",
            ),
        ),
    ]
