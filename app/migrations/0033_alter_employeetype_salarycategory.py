# Generated by Django 4.0.6 on 2022-07-29 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_role_delete_rolesalary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeetype',
            name='salaryCategory',
            field=models.CharField(choices=[('Fixed', 'Fixed'), ('Not Fixed', 'Not Fixed')], default='Not Fixed', max_length=9),
        ),
    ]
