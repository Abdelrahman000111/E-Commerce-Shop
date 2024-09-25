from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

def upload_image_category(instance , file_name):
    extension = file_name.split('.')[1]
    return f'Category/{instance.name}.{extension}'

def upload_image_product(instance , file_name):
    extension = file_name.split('.')[1]
    return f'Product/{instance.product_name}.{extension}'


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True , null = True , blank=True)
    image = models.ImageField(upload_to=upload_image_category, height_field=None, width_field=None, max_length=None)

    def save(self , *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category , self).save(*args , **kwargs)

    def get_url(self):
        return reverse('shop:category_slug' , args = [self.slug,])

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True , null = True , blank=True)
    description = models.TextField()
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to=upload_image_product, height_field=None, width_field=None, max_length=None)
    stock = models.IntegerField()
    is_available = models.BooleanField(default = True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self , *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product , self).save(*args , **kwargs)

    def get_url(self):
        return reverse('shop:product_details' , args = [self.category.slug , self.slug ,])

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return self.product_name



class Offer(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    ratio = models.IntegerField()
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def final_price(self):
        discount = (self.product.price * self.ratio) / 100
        final_price = self.product.price - discount
        return final_price

    class Meta:
        verbose_name = ("Offer")
        verbose_name_plural = ("Offers")

    def __str__(self):
        return str(self.product)




class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=150)
    size = models.CharField(max_length=150)
    created_at = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return f'{self.product} {self.color} {self.size}'


