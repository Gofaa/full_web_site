# Generated by Django 4.0 on 2023-02-26 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0006_news_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
    ]