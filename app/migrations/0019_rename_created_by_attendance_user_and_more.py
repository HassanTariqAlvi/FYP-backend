# Generated by Django 4.0.3 on 2022-07-12 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_remove_user_employee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='chemical',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='dailywork',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='employeetype',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='loan',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='loandetail',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='loanrecovery',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='measurecriteria',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='productprice',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='rolesalary',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='salary',
            old_name='created_by',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='salaryslip',
            old_name='created_by',
            new_name='user',
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]