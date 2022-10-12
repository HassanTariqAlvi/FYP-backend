# Generated by Django 4.0.6 on 2022-08-14 05:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0063_salarygeneration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salarygeneration',
            name='generate_datetime',
        ),
        migrations.AddField(
            model_name='salarygeneration',
            name='generate_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 14, 5, 38, 23, 125058, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salarygeneration',
            name='generate_time',
            field=models.TimeField(default=datetime.datetime(2022, 8, 14, 5, 38, 41, 813908, tzinfo=utc)),
            preserve_default=False,
        ),
    ]