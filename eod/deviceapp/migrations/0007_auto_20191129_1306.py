# Generated by Django 2.2.1 on 2019-11-29 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deviceapp', '0006_dangerlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dangerlog',
            name='avg_voc',
        ),
        migrations.RemoveField(
            model_name='devicelog',
            name='avg_voc',
        ),
        migrations.AddField(
            model_name='dangerlog',
            name='avg_co',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dangerlog',
            name='avg_lpg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dangerlog',
            name='avg_smoke',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='devicelog',
            name='avg_co',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='devicelog',
            name='avg_lpg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='devicelog',
            name='avg_smoke',
            field=models.FloatField(default=0.0),
        ),
    ]
