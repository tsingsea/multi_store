# Generated by Django 4.2.15 on 2024-08-29 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("stores", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttributeKey",
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
                ("key_name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name="storeattribute",
            name="attribute_key",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="stores.attributekey"
            ),
        ),
    ]
