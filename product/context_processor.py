from .models import Category , Offer

def category(request):
    categories = Category.objects.all()
    return {'categories':categories,}

def offers(request):
    offers = Offer.objects.all()
    return {'offers':offers,}