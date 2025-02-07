# Generated by Django 5.0.6 on 2024-06-05 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_quizcontent_assignment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quizcontent",
            name="assignment",
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.assignment",
            ),
            preserve_default=False,
        ),
    ]
