from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart,OrderItem
from inventory.models import Products
import json
from django.contrib import messages

#Cart Details
@login_required
def cart(request):
    if request.user.is_authenticated and request.user.profile.usertype == 'User':         
        customer = request.user
        order, created = Cart.objects.get_or_create(customer=customer, order_status=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_grand_total':0, 'get_cart_items': 0}
        return redirect('listing')
    
    context = {
        "title": "Your Cart | Konsultera",
        "items": items,
        'orders': order
    }
    return render(request, 'cart.html', context)

#Checkout function
@login_required
def checkout(request):
    customer = request.user
    order, created = Cart.objects.get_or_create(customer=customer, order_status=False)
    orderItem = OrderItem.objects.filter(ordered_by=order)
    for item in orderItem:
        product = Products.objects.get(pk=item.product.pk)
        if item.quantity > product.product_quantity:
            messages.warning(request,"One or more items exceed available quantity!")
            return redirect('listing')

    for item in orderItem:
        if(item.quantity<product.product_quantity):
            product.product_quantity = item.product.product_remaining
            product.save()
            orderItem.delete()
        elif(item.quantity==product.product_quantity):
            product.product_quantity = item.product.product_remaining
            product.product_status = "Inactive"
            product.save()
            orderItem.delete()
        else:
            messages.warning(request,"One or more items exceed available quantity!")
            return redirect('listing')
    
    messages.success(request, f'Your order was completed successfully!')
    return redirect('listing')


#Get inital cart
@login_required
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
    product.product_remaining = (product.product_remaining + orderItem.quantity)
    product.save()
    orderItem.delete()
    response['orderQty'] = -1
    response['availableQty'] = product.product_remaining
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

    #Only available in User Listing; Adds one unit of the item to user's cart
    if action == 'add':
        orderItem.quantity = (orderItem.quantity)
        product.product_remaining = (product.product_remaining - 1)
        product.save()
        orderItem.save()
    
    #Only available in Cart; Adds input amount of units to the user's cart 
    elif action == 'custom':
        #User chose to reduce items
        if orderItem.quantity>value and value >= 0:
            difference =  orderItem.quantity-value
            orderItem.quantity = (orderItem.quantity - (difference))
            product.product_remaining = (product.product_remaining + (difference))
            product.save()
            orderItem.save()
        #User chose to add items
        elif orderItem.quantity<value:
            difference =  value-orderItem.quantity
            orderItem.quantity = (orderItem.quantity + (difference))
            product.product_remaining = (product.product_remaining - (difference))
            product.save()
            orderItem.save()
        #When Input exceeds items in stock
        elif (value+product.product_remaining) > product.product_quantity:
            orderItem.quantity = product.product_remaining
            orderItem.save()
            product.product_remaining = 0
            product.save()
            
        else:
            pass
    else:
        pass

    response['orderQty'] = orderItem.quantity
    response['availableQty'] = product.product_remaining
    response['newTotal'] = float(orderItem.get_total)
    context = {
        "response": response,
        "cart_items":order.get_cart_items,
        "grand_total": float(order.get_grand_total)
    }
    return JsonResponse(context, safe=False)
