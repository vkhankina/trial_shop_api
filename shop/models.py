from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

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
    total = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))

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
    total = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f'{self.product.name}: {self.qty} pcs'

    @classmethod
    def list(cls, cart_id):
        return cls.objects.filter(cart_id=cart_id)

    @classmethod
    def add_to_cart(cls, cart, product, qty):
        # FIX: should be validation error
        if cart.state != Cart.CartState.NEW:
            raise Exception('Cart must be new!')

        item = cls._get_by_product_id(cart.id, product.id)
        if item:
            item.update(item.qty + qty)
        else:
            item = cls._create(cart, product, qty)
        return item

    def update(self, qty):
        # FIX: should be validation error
        if self.cart.state != Cart.CartState.NEW:
            raise Exception('Cart must be new!')

        if qty > 0:
            self.qty = qty
            self.total = self.product.price * qty
            self.save()
            self._update_cart_total()
        elif qty == 0:
            self._delete()
        else:
            # FIX: should be validation error
            raise Exception('CartItem qty is negative!')
        return self

    @classmethod
    def _get_by_product_id(cls, cart_id, product_id):
        return cls.objects.filter(
            cart_id=cart_id
        ).filter(
            product_id=product_id
        ).first()

    @classmethod
    def _create(cls, cart, product, qty):
        item = cls(
            cart=cart,
            product=product,
            qty=qty,
            total=product.price * qty
        )
        item.save()
        item._update_cart_total()
        return item

    def _delete(self):
        self.delete(keep_parents=True)
        self._update_cart_total()
        return self

    def _update_cart_total(self):
        self.cart.total = self.__class__.objects.filter(
            cart_id=self.cart_id
        ).aggregate(models.Sum('total'))['total__sum']
        self.cart.save()
