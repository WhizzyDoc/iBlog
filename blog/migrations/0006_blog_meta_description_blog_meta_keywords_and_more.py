# Generated by Django 4.1.4 on 2023-11-21 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment_active_tag_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='meta_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='featured',
            field=models.BooleanField(default=True),
        ),
    ]
