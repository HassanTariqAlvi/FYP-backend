# Generated by Django 4.0.6 on 2022-08-12 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_alter_user_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='app.usergroup', verbose_name='groups'),
        ),
    ]
