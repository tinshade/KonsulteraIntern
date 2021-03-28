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
        items_in_cart+=(str(each.product.pk)+"_")
    return JsonResponse({"cart_items":order.get_cart_items, "items": items_in_cart}, safe=False)


#Delete Items in Cart
@login_required
def remove_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    response = {"dataFor":productId, "orderQty": None, "availableQty": None, "newTotal": None}
    customer = request.user
    product = Products.objects.get(pk=productId)
    order, created = Cart.objects.get_or_create(customer=customer, order_status=False)
    orderItem, created = OrderItem.objects.get_or_create(ordered_by=order, product = product)
    product.product_quantity = (product.product_quantity + orderItem.quantity)
    product.save()
    orderItem.delete()
    response['orderQty'] = -1
    response['availableQty'] = product.product_quantity
    response['newTotal'] = float(orderItem.get_total)

    context = {
        "response": response,
        "cart_items":order.get_cart_items,
        "grand_total": float(order.get_grand_total)
    }
    return JsonResponse(context, safe=False)



#Update Items in Cart
@login_required
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    value = int(data['value'])
    response = {"dataFor":productId, "orderQty": None, "availableQty": None, "newTotal": None}
    customer = request.user
    product = Products.objects.get(pk=productId)
    order, created = Cart.objects.get_or_create(customer=customer, order_status=False)
    orderItem, created = OrderItem.objects.get_or_create(ordered_by=order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity)
        product.product_quantity = (product.product_quantity - 1)
        product.save()
        orderItem.save()
        response['orderQty'] = orderItem.quantity
        response['availableQty'] = product.product_quantity
    elif action == 'custom':
        #User chose to reduce items
        if orderItem.quantity>value and value >= 0:
            difference =  orderItem.quantity-value
            orderItem.quantity = (orderItem.quantity - (difference))
            product.product_remaining = (product.product_remaining + (difference))
            product.save()
            orderItem.save()
            response['orderQty'] = orderItem.quantity
            response['availableQty'] = product.product_remaining
            response['newTotal'] = float(orderItem.get_total)
        #User chose to add items
        elif orderItem.quantity<value:
            difference =  value-orderItem.quantity
            orderItem.quantity = (orderItem.quantity + (difference))
            product.product_remaining = (product.product_remaining - (difference))
            product.save()
            orderItem.save()
            response['orderQty'] = orderItem.quantity
            response['availableQty'] = product.product_remaining
            response['newTotal'] = float(orderItem.get_total)
        else:
            pass
    else:
        pass
    context = {
        "response": response,
        "cart_items":order.get_cart_items,
        "grand_total": float(order.get_grand_total)
    }
    return JsonResponse(context, safe=False)
