# Generated by Django 4.2 on 2023-07-24 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("productapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=100, verbose_name="name"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="available",
            field=models.BooleanField(default=True, verbose_name="available"),
        ),
        migrations.AddField(
            model_name="product",
            name="limited",
            field=models.BooleanField(default=False, verbose_name="limited"),
        ),
        migrations.AddField(
            model_name="tag",
            name="category",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tags",
                to="productapp.category",
                verbose_name="category",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="products",
                to="productapp.category",
                verbose_name="category",
            ),
        ),
    ]
