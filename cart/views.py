from django.shortcuts import redirect, render , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from category.models import Category
from .models import Cart_item,Coupon,Order,OrderProduct
from store.models import Product,Variation,Offer
# Create your views here.


@login_required(login_url='accounts:login')
def add_cart(request,product_id,cart_item_id=None):
    user = request.user
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        color = request.POST['color']
        size = request.POST['size']
        is_item_exist = Cart_item.objects.filter(user=user,product=product,vartions__color=color,vartions__size=size).exists()
        if is_item_exist:
            cart_item = Cart_item.objects.get(user=user,product=product,vartions__color=color,vartions__size=size)
            cart_item.quantity += 1
            cart_item.save()
            return redirect('cart:cart')
        else:
            variation = Variation.objects.create(product=product,color=color,size=size)
            variation.save()
            cart_item = Cart_item.objects.create(user=user,product=product,quantity = 1,vartions=variation)
            cart_item.save()
            return redirect('cart:cart')
    else:
        cart_item = Cart_item.objects.get(user=user,product=product,id=cart_item_id)
        if cart_item.quantity>=1:
            cart_item.quantity +=1
            cart_item.save()
            return redirect('cart:cart')        


def remove_cart_item(request,product_id,cart_item_id):
    product = Product.objects.get(id=product_id)
    cart_item = Cart_item.objects.get(product=product,user=request.user,id=cart_item_id)
    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart')

def remove_cart(request,product_id,cart_item_id):
    product = Product.objects.get(id=product_id)
    cart_item = Cart_item.objects.get(product=product,user=request.user,id=cart_item_id)
    cart_item.delete()
    return redirect('cart:cart')

def cart(request,subtotal=0,quantity=0,grand_total=0,coupon=None,discount=0):
    cart_items = Cart_item.objects.all().filter(user=request.user,is_active=True)
    for cart_item in cart_items:
        try:
            offer = Offer.objects.get(product = cart_item.product)
            new_price = offer.final_price()
            cart_item.product.price = new_price
            subtotal += new_price * cart_item.quantity
            quantity += cart_item.quantity
        except:
            subtotal += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

    if request.method == "POST":
        discount = request.POST['coupon']
        if discount:
            try:
                coupon = Coupon.objects.get(value=discount)
                shipping = 20   
                grand_total = shipping+subtotal 
                discount = (grand_total*coupon.ratio)/100
                grand_total = grand_total-discount
                cart_item.coupon = coupon
                cart_item.save()
            except:
                pass 
    else:            
        shipping = 20   
        grand_total = shipping+subtotal 


    context = {
        'cart_items':cart_items,
        'total':subtotal,
        'quantity':quantity,
        'grand_total':grand_total,
        'shipping': shipping,
        'discount':discount,
    }
    return render(request,'cart/cart.html',context)



def checkout(request,total=0,quantity=0,grand_total=0,address2=None):
    cart_items = Cart_item.objects.all().filter(user=request.user,is_active=True)
    for cart_item in cart_items:
        try:
            offer = Offer.objects.get(product = cart_item.product) # Offer With Coupon
            new_price = offer.final_price()
            cart_item.product.price = new_price
            total += new_price * cart_item.quantity
            quantity += cart_item.quantity
            shipping = 20
            grand_total = shipping + total
            if cart_item.coupon:
                discount = (grand_total * cart_item.coupon.ratio) / 100
                grand_total -= discount
            else:
                grand_total = shipping + total # Offer Without Coupon
        except:
            total += cart_item.product.price * cart_item.quantity # No Offer But With Coupon
            quantity += cart_item.quantity
            shipping = 20
            grand_total = shipping + total
            if cart_item.coupon:
                discount = (grand_total * cart_item.coupon.ratio) / 100
                grand_total -= discount
            else:
                grand_total = shipping + total # No Offer And Coupon
    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        phone = request.POST['phone']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        order = Order.objects.create(
            user = request.user,
            f_name = f_name,
            l_name = l_name,
            phone = phone,
            address1 = address1,
            address2 = address2,
            city = city,
            order_total = grand_total,
            is_active = True,
        )
        order.address2 = address2 if address2 else 'Not Entered'
        order.save()
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.user_id = request.user.id
            orderproduct.product = item.product
            orderproduct.variations = item.vartions
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()
            product = Product.objects.get(id = item.product.id)
            product.stock -= item.quantity
            product.save()
        Cart_item.objects.all().filter(user=request.user).delete()
        return redirect('home')
    context = {
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'shipping':shipping,
        'grand_total':grand_total,
    }
    return render(request , 'cart/checkout.html' , context)


