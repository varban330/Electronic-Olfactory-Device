# Generated by Django 2.2.1 on 2019-10-20 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deviceapp', '0005_devicelog_pushed'),
    ]

    operations = [
        migrations.CreateModel(
            name='DangerLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_temp', models.FloatField()),
                ('avg_voc', models.FloatField()),
                ('avg_pres', models.FloatField()),
                ('smell_class', models.CharField(max_length=100)),
                ('pushed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='danger_id_log', to='deviceapp.Device')),
            ],
        ),
    ]