from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    @classmethod
    def list(cls, **kwargs):
        order_by = kwargs.get('order_by')
        search = kwargs.get('search')

        query = cls.objects

        if search:
            condition = models.Q(name__icontains=search) | models.Q(code__icontains=search)
            query = query.filter(condition)

        if order_by:
            query = query.order_by(order_by)

        return query.all()


class Cart(models.Model):
    class CartState(models.TextChoices):
        NEW = 'new', _('new')
        EXPIRED = 'expired', _('expired')
        SOLD = 'sold', _('sold')

    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=CartState.choices, default=CartState.NEW, max_length=7)

    def __str__(self):
        return self.state

    @classmethod
    def create(cls):
        cart = cls()
        cart.save()
        return cart

    @classmethod
    def get(cls, p_key):
        return cls.objects.get(pk=p_key)

    def checkout(self):
        self.state = self.CartState.SOLD
        self.save()
        return self


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    qty = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.product.name}: {self.qty} pcs'
