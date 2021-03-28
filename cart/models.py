from django.db import models
from inventory.models import Products
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    order_status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.customer}'s Cart"
    
    @property
    def get_grand_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    ordered_by = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.product_price * self.quantity
        return total

    def __str__(self):
        return str(self.id)