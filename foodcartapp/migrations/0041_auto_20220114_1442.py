# Generated by Django 3.2 on 2022-01-14 11:42

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_rename_fistname_order_firstname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(max_length=200, verbose_name='адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='firstname',
            field=models.CharField(max_length=50, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='lastname',
            field=models.CharField(max_length=50, verbose_name='фамилия'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='телефон'),
        ),
    ]
