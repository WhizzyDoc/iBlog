# Generated by Django 4.1.4 on 2023-11-21 22:03

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_site_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]