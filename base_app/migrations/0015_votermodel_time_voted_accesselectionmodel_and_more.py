# Generated by Django 5.0.6 on 2024-07-09 12:18

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0014_votermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='votermodel',
            name='time_voted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AccessElectionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_time', models.DateField(auto_now_add=True)),
                ('election_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_app.electorialcommissionofficermodel')),
            ],
        ),
        migrations.CreateModel(
            name='StartEctionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateField(auto_now_add=True)),
                ('end_time', models.DateField()),
                ('election_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_app.electorialcommissionofficermodel')),
            ],
        ),
    ]
