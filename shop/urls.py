from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.products, name='products'),
    path('products/<int:product_id>', views.product, name='product'),
    path('cart/<int:cart_id>', views.cart, name='cart'),
    path('cart/create', views.create_cart, name='create_cart'),  # shouldn't be POST?
    path('cart/<int:cart_id>/items', views.cart_items, name='cart_items'),
    path('cart/<int:cart_id>/add', views.add_to_cart, name='add_to_cart'),  # POST?
    path('cart/items/<int:cart_item_id>', views.update_cart_item, name='update_cart_item')  # PATCH?
]
