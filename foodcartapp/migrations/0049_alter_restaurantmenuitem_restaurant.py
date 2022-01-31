# Generated by Django 3.2 on 2022-01-30 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_auto_20220130_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantmenuitem',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_items', to='foodcartapp.restaurant', verbose_name='ресторан'),
        ),
    ]