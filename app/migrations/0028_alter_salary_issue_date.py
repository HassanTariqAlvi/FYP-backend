# Generated by Django 4.0.6 on 2022-07-26 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_delete_chemical'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='issue_date',
            field=models.DateField(),
        ),
    ]
