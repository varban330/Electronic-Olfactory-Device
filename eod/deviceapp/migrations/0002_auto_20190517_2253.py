# Generated by Django 2.2.1 on 2019-05-17 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deviceapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_id',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
