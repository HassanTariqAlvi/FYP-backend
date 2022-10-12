# Generated by Django 4.0.3 on 2022-06-29 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_loan_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.IntegerField(default=1)),
                ('updated_by', models.IntegerField(default=1)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=8),
        ),
        migrations.AddField(
            model_name='employeetype',
            name='salaryCategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='app.salarycategory'),
            preserve_default=False,
        ),
    ]