# Generated by Django 5.0.1 on 2024-02-03 07:24

import django_extensions.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0002_alter_tag_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=models.CharField(
                help_text="Enter a unique HEX value",
                max_length=7,
                unique=True,
                validators=[django_extensions.validators.HexValidator(length=7)],
                verbose_name="colour",
            ),
        ),
    ]
