# Generated by Django 4.0.6 on 2022-08-16 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0073_alter_loanrecovery_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loandetail',
            options={'permissions': [('generateReport_loandetail', 'Can generate loan detail report')]},
        ),
    ]
