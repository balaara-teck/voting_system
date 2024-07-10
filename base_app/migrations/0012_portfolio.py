# Generated by Django 5.0.6 on 2024-07-06 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0011_delete_electiondaymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio_name', models.CharField(max_length=255)),
                ('election_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_app.electorialcommissionofficermodel')),
            ],
        ),
    ]
