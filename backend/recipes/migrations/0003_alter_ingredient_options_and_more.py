# Generated by Django 5.0.1 on 2024-02-05 18:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0002_ingredient"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ingredient",
            options={
                "ordering": ("name",),
                "verbose_name": "ingredient",
                "verbose_name_plural": "ingredients",
            },
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="measurement_unit",
            field=models.CharField(
                help_text="In grams, pieces, to taste, etc",
                max_length=200,
                verbose_name="measurement unit",
            ),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(
                help_text="Enter an ingredient to add",
                max_length=200,
                verbose_name="ingredient name",
            ),
        ),
    ]