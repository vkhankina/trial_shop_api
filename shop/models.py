from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.TextField()


class Cart(models.Model):
    class CartState(models.TextChoices):
        NEW = 'new', _('new')
        EXPIRED = 'expired', _('expired')
        SOLD = 'sold', _('sold')

    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=CartState.choices, default=CartState.NEW, max_length=7)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    qty = models.IntegerField(default=1, validators=[MinValueValidator(0)])
