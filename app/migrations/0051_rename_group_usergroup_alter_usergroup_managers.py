# Generated by Django 4.0.6 on 2022-08-11 18:30

import app.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0050_group'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Group',
            new_name='UserGroup',
        ),
        migrations.AlterModelManagers(
            name='usergroup',
            managers=[
                ('objects', app.managers.UserGroupManager()),
            ],
        ),
    ]
