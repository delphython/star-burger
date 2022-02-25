from collections import Counter, defaultdict
from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from foodcartapp.models import (
    Product,
    Restaurant,
    Order,
)
from places.geo_coder import get_distance


class Login(forms.Form):
    username = forms.CharField(
        label="Логин",
        max_length=75,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Укажите имя пользователя",
            }
        ),
    )
    password = forms.CharField(
        label="Пароль",
        max_length=75,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={"form": form})

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(
            request,
            "login.html",
            context={
                "form": form,
                "ivalid": True,
            },
        )


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("restaurateur:login")


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url="restaurateur:login")
def view_products(request):
    restaurants = list(Restaurant.objects.order_by("name"))
    products = list(Product.objects.prefetch_related("menu_items"))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:

        availability = {
            **default_availability,
            **{
                item.restaurant_id: item.availability
                for item in product.menu_items.all()
            },
        }
        orderer_availability = [
            availability[restaurant.id] for restaurant in restaurants
        ]

        products_with_restaurants.append((product, orderer_availability))

    return render(
        request,
        template_name="products_list.html",
        context={
            "products_with_restaurants": products_with_restaurants,
            "restaurants": restaurants,
        },
    )


@user_passes_test(is_manager, login_url="restaurateur:login")
def view_restaurants(request):
    return render(
        request,
        template_name="restaurants_list.html",
        context={
            "restaurants": Restaurant.objects.all(),
        },
    )


@user_passes_test(is_manager, login_url="restaurateur:login")
def view_orders(request):
    distance_to_restaurant = []
    order_items = []
    temp_products_in_restaurants = defaultdict(list)

    orders = (
        Order.objects.prefetch_related("order_products__product")
        .select_related("restaurant")
        .annotate_order_cost()
    )

    for order in orders:
        products_in_restaurants = {}
        restaurants_with_all_products = []

        for product_item in order.order_products.all():
            for restaurant_item in product_item.product.menu_items.all():
                temp_products_in_restaurants[product_item.product].append(
                    restaurant_item.restaurant
                )
        products_in_restaurants = dict(temp_products_in_restaurants)
        for restaurants in products_in_restaurants.values():
            if restaurants_with_all_products:
                restaurants_with_all_products = list(
                    (
                        Counter(restaurants_with_all_products)
                        & Counter(restaurants_with_all_products)
                    ).elements()
                )
            else:
                restaurants_with_all_products = restaurants

        for restaurant in restaurants_with_all_products:
            distance = get_distance(restaurant.address, order.address)
            distance_to_restaurant.append(
                f"{distance} км." if distance else "расстояние неизвестно"
            )

        restaurant_with_distance = dict(
            zip(restaurants_with_all_products, distance_to_restaurant)
        )

        sorted_restaurant_with_distance_keys = sorted(
            restaurant_with_distance, key=restaurant_with_distance.get
        )

        sorted_restaurant_with_distance = {
            key: restaurant_with_distance[key]
            for key in sorted_restaurant_with_distance_keys
        }

        order_items.append(
            {
                "id": order.id,
                "order_status": order.get_order_status_display,
                "order_cost": order.order_cost,
                "firstname": order.firstname,
                "lastname": order.lastname,
                "phonenumber": order.phonenumber,
                "address": order.address,
                "comment": order.comment,
                "payment_method": order.get_payment_method_display,
                "restaurants": sorted_restaurant_with_distance,
            }
        )

    return render(
        request,
        template_name="order_items.html",
        context={
            "order_items": order_items,
        },
    )
