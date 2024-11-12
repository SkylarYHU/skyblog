# Generated by Django 5.1.3 on 2024-11-11 11:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_post_likes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="likes",
        ),
        migrations.AddField(
            model_name="post",
            name="like_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]