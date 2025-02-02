# Generated by Django 3.2 on 2022-02-05 09:54

from django.db import migrations


class Migration(migrations.Migration):
    def set_order_products_price(apps, schema_editor):
        OrderProducts = apps.get_model("foodcartapp", "OrderProducts")
        orderproducts_set = OrderProducts.objects.select_related(
            "product"
        ).all()
        for orderproduct in orderproducts_set.iterator():
            orderproduct.price = orderproduct.product.price
            orderproduct.save()

    dependencies = [
        ("foodcartapp", "0055_auto_20220204_1735"),
    ]

    operations = [
        migrations.RunPython(set_order_products_price),
    ]
