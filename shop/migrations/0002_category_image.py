# Generated by Django 4.1.2 on 2022-11-07 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to='categories/%Y/%m%d'),
        ),
    ]