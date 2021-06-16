# Generated by Django 2.2.21 on 2021-06-16 09:07

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_removed",
                    models.BooleanField(
                        default=False,
                        help_text="Soft Deleted.",
                        verbose_name="Is removed",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
            ],
            options={
                "verbose_name": "Book",
                "verbose_name_plural": "Books",
            },
            managers=[
                ("active_objects", django.db.models.manager.Manager()),
            ],
        ),
    ]
