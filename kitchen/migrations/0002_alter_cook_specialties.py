# Generated by Django 5.0.6 on 2024-07-04 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kitchen", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cook",
            name="specialties",
            field=models.ManyToManyField(
                blank=True, related_name="specialty_cooks", to="kitchen.dishtype"
            ),
        ),
    ]
