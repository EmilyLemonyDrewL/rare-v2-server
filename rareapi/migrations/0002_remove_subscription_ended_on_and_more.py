# Generated by Django 4.1.3 on 2024-06-12 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='ended_on',
        ),
        migrations.AlterField(
            model_name='rareuser',
            name='created_on',
            field=models.DateField(auto_now=True),
        ),
    ]
