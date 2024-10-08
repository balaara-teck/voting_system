# Generated by Django 5.0.6 on 2024-07-28 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0016_accesselectionmodel_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesselectionmodel',
            name='election_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='accesselectionmodel',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='accesselectionmodel',
            name='voter_id',
            field=models.CharField(max_length=10),
        ),
    ]
