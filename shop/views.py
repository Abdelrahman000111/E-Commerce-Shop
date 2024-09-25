from django.shortcuts import render , get_object_or_404
from product.models import Product , Category , Offer
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def shop(request , category_slug = None):

    if category_slug != None:
        category = get_object_or_404(Category , slug=category_slug)
        products = Product.objects.all().filter(category=category , is_available = True)

    else:
        products = Product.objects.all().filter(is_available = True)

    paginator = Paginator(products , 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    
    context = {
        'products': page_obj
    }


    return render(request , 'shop/shop.html' , context)

def product_details(request , category_slug , product_slug , offer = None):
    category = Category.objects.get(slug=category_slug)
    product = Product.objects.get(slug=product_slug , category=category)

    try:
        offer = Offer.objects.get(product = product)
    except:
        pass

    context = {
        'product':product,
        'offer':offer,
    }

    return render(request , 'shop/product_details.html',context)

def offers(request):
    return render(request , 'shop/offers.html')


def search(request):
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        products = Product.objects.order_by('-created_at').filter(Q(description__icontains = keywords)|Q(product_name = keywords))
        context = {
        'products': products,
        }
        return render(request , 'shop/search.html' , context)