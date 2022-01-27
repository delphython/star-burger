from django.db import models
from django.db.models import Sum, F
from django.core.validators import MinValueValidator
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField("название", max_length=50)
    address = models.CharField(
        "адрес",
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        "контактный телефон",
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = "ресторан"
        verbose_name_plural = "рестораны"

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = RestaurantMenuItem.objects.filter(
            availability=True
        ).values_list("product")
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField("название", max_length=50)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("название", max_length=50)
    category = models.ForeignKey(
        ProductCategory,
        verbose_name="категория",
        related_name="products",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        "цена",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField("картинка")
    special_status = models.BooleanField(
        "спец.предложение",
        default=False,
        db_index=True,
    )
    description = models.TextField(
        "описание",
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name="menu_items",
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="menu_items",
        verbose_name="продукт",
    )
    availability = models.BooleanField(
        "в продаже", default=True, db_index=True
    )

    class Meta:
        verbose_name = "пункт меню ресторана"
        verbose_name_plural = "пункты меню ресторана"
        unique_together = [["restaurant", "product"]]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def annotate_order_cost(self):
        return self.annotate(
            order_cost=Sum(
                F("order_products__quantity")
                * F("order_products__product__price")
            )
        )


class Order(models.Model):
    firstname = models.CharField(
        "имя",
        max_length=50,
    )
    lastname = models.CharField(
        "фамилия",
        max_length=50,
    )
    phonenumber = PhoneNumberField(
        "телефон",
    )
    address = models.TextField(
        "адрес доставки",
        blank=True,
    )
    ORDER_STATUSES_CHOICES = [
        ("НО", "Необработан"),
        ("ГО", "Готовится"),
        ("ГВ", "Готов"),
        ("ДО", "Доставляется"),
        ("ДН", "Доставлен"),
        ("ОН", "Отменен"),
    ]
    status = models.CharField(
        "статус заказа",
        max_length=2,
        choices=ORDER_STATUSES_CHOICES,
        default="НО",
        db_index=True,
    )
    comment = models.TextField(
        "комментарий",
        blank=True,
    )
    creation_time = models.DateTimeField(
        "время создания",
        default=timezone.now,
        db_index=True,
    )
    call_date = models.DateTimeField(
        "дата звонка",
        blank=True,
        null=True,
        db_index=True,
    )
    delivery_date = models.DateTimeField(
        "дата доставки",
        blank=True,
        null=True,
        db_index=True,
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"Заказ № {self.id} для {self.firstname} {self.lastname}"


class OrderProducts(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_products",
        verbose_name="заказ",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_orders",
        verbose_name="товар",
    )
    quantity = models.PositiveIntegerField(
        "количество",
    )
    price = models.DecimalField(
        "цена",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name = "товар в заказе"
        verbose_name_plural = "товары в заказе"
        unique_together = [["order", "product"]]

    def __str__(self):
        return f"Заказ №{self.order.id}: товар {self.product.name}"
