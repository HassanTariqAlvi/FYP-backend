# Generated by Django 4.0.6 on 2022-08-15 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0067_alter_attendance_options_alter_dailywork_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailywork',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]