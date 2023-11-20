# Generated by Django 4.2.7 on 2023-11-19 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blog_featured_tag_blog_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
