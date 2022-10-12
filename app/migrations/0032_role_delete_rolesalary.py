# Generated by Django 4.0.6 on 2022-07-29 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_alter_dailywork_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('salary', models.IntegerField()),
                ('employeeType', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.employeetype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='RoleSalary',
        ),
    ]