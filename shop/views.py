from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Product


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
