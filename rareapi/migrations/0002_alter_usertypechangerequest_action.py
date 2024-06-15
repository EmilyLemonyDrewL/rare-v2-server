# Generated by Django 4.1.3 on 2024-06-13 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rareapi", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usertypechangerequest",
            name="action",
            field=models.CharField(
                choices=[("promotion", "Promotion"), ("demotion", "Demotion")],
                default="promotion",
                max_length=10,
            ),
        ),
    ]
