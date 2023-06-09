# Generated by Django 4.1.7 on 2023-03-26 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tache",
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
                ("tache_text", models.CharField(max_length=200)),
                ("frequence_int", models.PositiveIntegerField()),
                ("last_date", models.DateTimeField(verbose_name="date published")),
                ("duration", models.DurationField()),
            ],
        ),
    ]
