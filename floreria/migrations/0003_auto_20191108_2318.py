# Generated by Django 2.2.6 on 2019-11-09 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floreria', '0002_flores_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='flores',
            name='estado',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flores',
            name='stock',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]