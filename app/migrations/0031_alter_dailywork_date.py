# Generated by Django 4.0.6 on 2022-07-28 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_alter_dailywork_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailywork',
            name='date',
            field=models.DateField(),
        ),
    ]