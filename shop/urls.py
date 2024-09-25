from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('' , views.shop , name = 'shop'),
    path('offers/' , views.offers , name = 'offers'),
    path('search/' , views.search , name = 'search'),
    path('<str:category_slug>/' , views.shop , name = 'category_slug'),
    path('<str:category_slug>/<str:product_slug>/' , views.product_details , name = 'product_details'),
]