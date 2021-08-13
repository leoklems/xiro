# Generated by Django 3.2.6 on 2021-08-30 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0003_auto_20210829_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='post/images/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
