# Generated by Django 3.2.6 on 2021-08-29 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_post_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='categories',
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, related_name='post_categories', to='contents.PostCategory'),
        ),
    ]
