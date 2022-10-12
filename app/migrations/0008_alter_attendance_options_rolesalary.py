# Generated by Django 4.0.3 on 2022-07-02 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_employeetype_salarycategory_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'ordering': ['date']},
        ),
        migrations.CreateModel(
            name='RoleSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.IntegerField(default=1)),
                ('updated_by', models.IntegerField(default=1)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('salary', models.IntegerField()),
                ('employeeType', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.employeetype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
