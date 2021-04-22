from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Product, Cart, CartItem


def product(request, product_id):
    entity = get_object_or_404(Product, id=product_id)
    return JsonResponse(model_to_dict(entity))


def products(request):
    search = request.GET.get('search')
    order_by = request.GET.get('order_by')

    if order_by:
        order_by_parsed = order_by.split(':')
        # FIX: check also if field is present in model
        if len(order_by_parsed) == 2 and order_by_parsed[1] == 'desc':
            order_by = f'-{order_by_parsed[0]}'
        elif len(order_by_parsed) == 2 and order_by_parsed[1] == 'asc':
            order_by = order_by_parsed[0]
        else:
            return JsonResponse({'error': 'Unprocessable entity'}, 422)

    entities = Product.list(search=search, order_by=order_by)
    return JsonResponse([model_to_dict(e) for e in entities], safe=False)


def cart(request, cart_id):
    entity = get_object_or_404(Cart, id=cart_id)
    return JsonResponse(model_to_dict(entity))


def create_cart(request):
    entity = Cart.create()
    return JsonResponse(model_to_dict(entity))


def cart_items(request, cart_id):
    entities = CartItem.list(cart_id)
    return JsonResponse([model_to_dict(e) for e in entities], safe=False)


def add_to_cart(request, cart_id):
    product_id = request.POST['product_id']
    qty = request.POST.get('qty', 1)

    product_entity = get_object_or_404(Product, id=product_id)
    cart_entity = get_object_or_404(Cart, id=cart_id)

    cart_item = CartItem.add_to_cart(cart_entity, product_entity, qty)
    return JsonResponse(model_to_dict(cart_item))


def update_cart_item(request, cart_item_id):
    qty = request.POST['qty']

    entity = get_object_or_404(CartItem, id=cart_item_id)
    entity.update(qty)
    return JsonResponse(model_to_dict(entity))
