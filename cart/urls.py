from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [

    path('',views.cart,name='cart'),
    path('add/<int:product_id>/',views.add_cart,name='add_cart'),
    path('add/<int:product_id>/<int:cart_item_id>/',views.add_cart,name='add_cart'),
    path('remove/<int:product_id>/<int:cart_item_id>/',views.remove_cart_item,name='remove_cart_item'),
    path('removecart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
    path('checkout/',views.checkout,name='checkout'),
    # path('offers_in_cart/<int:product_id>/',views.offers_in_cart,name='offers_in_cart'),
    
]
