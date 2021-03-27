from django.contrib import admin
from .models import Cart, OrderItem

admin.site.register(Cart)
admin.site.register(OrderItem)