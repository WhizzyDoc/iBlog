# Generated by Django 4.1.4 on 2023-11-22 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blog_meta_description_blog_meta_keywords_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategory',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
