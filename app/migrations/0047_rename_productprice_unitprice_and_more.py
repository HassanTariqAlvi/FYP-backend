# Generated by Django 4.0.6 on 2022-08-11 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_rename_product_unit_rename_product_productprice_unit_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductPrice',
            new_name='UnitPrice',
        ),
        migrations.RenameField(
            model_name='dailywork',
            old_name='product_price',
            new_name='unit_price',
        ),
    ]