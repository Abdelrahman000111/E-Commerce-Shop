from django.contrib import admin
from . models import Product , Category , Offer , Variation
# Register your models here.

@admin.register(Category)
class CateoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name' , 'price' , 'category' , 'created_at' , 'modified_at' , 'is_available']
    list_display_links = ['product_name' , 'price']
    list_editable = ['category']

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['product' , 'ratio' , 'created_at' , 'modified_at' , 'is_active']
    list_display_links = ['product']
    list_editable = ['ratio']

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product' , 'color' , 'size' ,'created_at']
    list_display_links = ['product']
    list_editable = ['color' , 'size']

admin.site.site_header = 'E-Commerce'
admin.site.site_title = 'E-Commerce'
