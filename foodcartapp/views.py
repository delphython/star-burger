from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer


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
<<<<<<< HEAD
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
=======
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
>>>>>>> 6a2ad35fdf741a554800b7012eecc321be4192fa
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


class OrderProductsSerializer(ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = [
            "product",
            "quantity",
            "price",
        ]


class OrderSerializer(ModelSerializer):
    products = OrderProductsSerializer(
        many=True, write_only=True, allow_empty=False
    )

    class Meta:
        model = Order
        fields = [
            "firstname",
            "lastname",
            "phonenumber",
            "address",
            "products",
        ]


@transaction.atomic
@api_view(["POST"])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    order = Order.objects.create(
        firstname=serializer.validated_data["firstname"],
        lastname=serializer.validated_data["lastname"],
        phonenumber=serializer.validated_data["phonenumber"],
        address=serializer.validated_data["address"],
    )

    products = serializer.validated_data["products"]

    OrderProducts.objects.bulk_create(
        [
            OrderProducts(
                order=order,
                product=product["product"],
                quantity=product["quantity"],
                price=product["product"].price,
            )
            for product in products
        ]
    )

    return Response(serializer.data, status=201)
