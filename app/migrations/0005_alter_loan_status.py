# Generated by Django 4.0.3 on 2022-06-25 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_loan_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved')], default='Pending', max_length=8),
        ),
    ]
