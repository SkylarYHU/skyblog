# Generated by Django 5.1.3 on 2024-11-11 11:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_remove_post_likes_post_like_count"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="like_count",
        ),
    ]