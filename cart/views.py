from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart,OrderItem

#Cart Details
@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Cart.objects.get_or_create(customer=customer, order_status=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_grand_total':0, 'get_cart_items': 0}
    
    context = {
        "title": "Your Cart | Konsultera",
        "items": items,
        'orders': order,
    }
    return render(request, 'cart.html', context)

#Checkout function
def checkout(request):
    context =  {
        {"title": 'Checkout Order | Konsultera'},
    }
    return render(request, 'checkout.html', context)

#Update Items in Cart
@login_required
def update_cart(request, pk):
    return JsonResponse('Item Added to cart', safe=False)
