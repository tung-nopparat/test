# Generated by Django 4.1.4 on 2023-01-28 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_alter_blog_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='view',
            field=models.IntegerField(default=0, null=True),
        ),
    ]