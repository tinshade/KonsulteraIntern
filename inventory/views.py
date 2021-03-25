from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CRUDProductForm
from .models import Products
from django.http import HttpResponseForbidden


#Landing Page
@login_required
def listing(request):
    products = Products.objects.filter(product_owner=request.user)
    context = {
        'products':products,
        "title": "Products Listing | Konsultera"
    }
    return render(request, 'listing.html', context)


@login_required
def crud_product(request, pk=None):
    if pk:
        title = "Edit Product | Konsultera"
        product = get_object_or_404(Products, pk=pk)
        if product.product_owner != request.user:
            return HttpResponseForbidden()
    else:
        title = "Add Products | Konsultera"
        product = Products(product_owner = request.user)
    
    form = CRUDProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Operation successful!")
        return redirect('listing')
    context={
        "title": title,
        "form":form,
        "pk":pk
    }
    return render(request, 'cruditem.html', context)

@login_required
def delete_item(request,pk):
    Products.objects.filter(id=pk).delete()
    messages.success(request, "Product was deleted successfully!")
    items = Products.objects.filter(product_owner=request.user)
    return redirect('listing')