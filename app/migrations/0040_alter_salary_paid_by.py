# Generated by Django 4.0.6 on 2022-08-02 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_alter_salary_options_alter_dailywork_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='paid_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='paid_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
