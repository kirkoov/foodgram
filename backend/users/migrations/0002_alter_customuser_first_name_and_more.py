# Generated by Django 5.0.2 on 2024-02-07 12:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(verbose_name="first name"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(verbose_name="last name"),
        ),
    ]