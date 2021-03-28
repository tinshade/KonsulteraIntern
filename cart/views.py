from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart,OrderItem
from inventory.models import Products
import json


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
        'orders': order
    }
    return render(request, 'cart.html', context)

#Checkout function
def checkout(request):
    context =  {
        {"title": 'Checkout Order | Konsultera'},
    }
    return render(request, 'checkout.html', context)


#Get inital cart
def get_items(request):
    customer = request.user
    order, created = Cart.objects.get_or_create(customer=customer, order_status=False)
    orderItem = OrderItem.objects.filter(ordered_by=order)
    items_in_cart = ""
    for each in orderItem:
        items_in_cart+=str(each)
    return JsonResponse({"cart_items":order.get_cart_items, "items": items_in_cart}, safe=False)

#Update Items in Cart
@login_required
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    orderItemStatus = {"status": None, "reason":""}
    productInvStatus = {"status": None, "reason":""}

    customer = request.user
    product = Products.objects.get(pk=productId)
    order, created = Cart.objects.get_or_create(customer=customer, order_status=False)
    orderItem, created = OrderItem.objects.get_or_create(ordered_by=order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        product.product_quantity = (product.product_quantity - 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        product.product_quantity = (product.product_quantity + 1)
    else:
        orderItem.quantity = (orderItem.quantity + 1)
        product.product_quantity = (product.product_quantity - 1)

    product.save()
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
        orderItemStatus['status']:False
        orderItemStatus['reason']:"Selected quantity reached zero."
    
    if product.product_quantity <= 0:
        productInvStatus['status']:False
        productInvStatus['reason']:"Inventory has ran out of items."


    context = {
        "orderItemStatus": orderItemStatus,
        "productInvStatus": productInvStatus,
        "cart_items":order.get_cart_items
    }
    return JsonResponse(context, safe=False)
