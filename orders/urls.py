from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/',
         views.cancel_order, name='cancel_order'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/',
         views.order_confirmation, name='order_confirmation'),
]
