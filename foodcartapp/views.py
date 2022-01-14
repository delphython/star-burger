import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .models import Product
from .models import Order
from .models import OrderProducts


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse(
        [
            {
                "title": "Burger",
                "src": static("burger.jpg"),
                "text": "Tasty Burger at your door step",
            },
            {
                "title": "Spices",
                "src": static("food.jpg"),
                "text": "All Cuisines",
            },
            {
                "title": "New York",
                "src": static("tasty.jpg"),
                "text": "Food is incomplete without a tasty dessert",
            },
        ],
        safe=False,
        json_dumps_params={
            "ensure_ascii": False,
            "indent": 4,
        },
    )


def product_list_api(request):
    products = Product.objects.select_related("category").available()

    dumped_products = []
    for product in products:
        dumped_product = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "special_status": product.special_status,
            "description": product.description,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
            },
            "image": product.image.url,
            "restaurant": {
                "id": product.id,
                "name": product.name,
            },
        }
        dumped_products.append(dumped_product)
    return JsonResponse(
        dumped_products,
        safe=False,
        json_dumps_params={
            "ensure_ascii": False,
            "indent": 4,
        },
    )


@api_view(["POST"])
def register_order(request):
    order_properties = request.data
    print(order_properties)

    if ("products") not in order_properties.keys():
        return Response({"error": "Data have no keys: products"})
    if ("firstname") not in order_properties.keys():
        return Response({"error": "Data have no keys: firstname"})
    if ("lastname") not in order_properties.keys():
        return Response({"error": "Data have no keys: lastname"})
    if ("phonenumber") not in order_properties.keys():
        return Response({"error": "Data have no keys: phonenumber"})
    if ("address") not in order_properties.keys():
        return Response({"error": "Data have no keys: phonenumber"})

    products = order_properties["products"]

    if (
        not isinstance(order_properties["firstname"], str)
        or not order_properties["firstname"]
    ):
        return Response({"error": "Firstname is not the str or not present"})
    if (
        not isinstance(order_properties["lastname"], str)
        or not order_properties["lastname"]
    ):
        return Response({"error": "Lastname is not the str or not present"})
    if (
        not isinstance(order_properties["phonenumber"], str)
        or not order_properties["phonenumber"]
    ):
        return Response({"error": "Phonenumber is not the str or not present"})
    if (
        not isinstance(order_properties["address"], str)
        or not order_properties["lastname"]
    ):
        return Response({"error": "Address is not the str or not present"})

    if not isinstance(products, list) or not products:
        return Response({"error": "Products is not the list or not present"})
    if isinstance(products, type(None)):
        return Response({"error": "Products list is empty"})

    order = Order(
        fistname=order_properties["firstname"],
        lastname=order_properties["lastname"],
        phonenumber=order_properties["phonenumber"],
        address=order_properties["address"],
    )
    order.save()

    for product in products:
        OrderProducts(
            order=order,
            product=get_object_or_404(Product, pk=product["product"]),
            quantity=product["quantity"],
        ).save()

    return Response("just a test", status=status.HTTP_201_CREATED)
    # JsonResponse({})
