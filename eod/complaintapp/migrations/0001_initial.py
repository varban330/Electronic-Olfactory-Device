# Generated by Django 2.2.1 on 2019-05-18 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('deviceapp', '0003_auto_20190518_1806'),
        ('authapp', '0002_auto_20190518_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('desc', models.CharField(max_length=1000)),
                ('is_resolved', models.BooleanField(default=False)),
                ('device', models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='device_id_complaint', to='deviceapp.Device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id_complaint', to='authapp.EndUser')),
            ],
        ),
    ]