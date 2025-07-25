# Generated by Django 5.2 on 2025-04-25 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scenic", "0006_alter_attraction_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attraction",
            name="category",
            field=models.SmallIntegerField(
                choices=[
                    (1, "Natural"),
                    (2, "Historical"),
                    (3, "Cultural"),
                    (4, "entertaining"),
                ],
                verbose_name="景点类别",
            ),
        ),
    ]
