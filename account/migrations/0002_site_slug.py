# Generated by Django 4.2.7 on 2023-11-19 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]