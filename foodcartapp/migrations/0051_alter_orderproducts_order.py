# Generated by Django 3.2 on 2022-01-31 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0050_alter_restaurantmenuitem_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproducts',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='foodcartapp.order', verbose_name='заказ'),
        ),
    ]