from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()
class Products(models.Model):
    product_owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE, blank=False, null=False)
    product_name = models.CharField(max_length=150, blank=False)
    product_price = models.FloatField(default=0.0, blank=False)
    product_quantity = models.PositiveIntegerField(default=0, blank=False)
    product_remaining = models.PositiveIntegerField(default=0, blank=False)
    choices = (("Active",'Active'), ("Inactive",'Inactive'))
    product_status = models.CharField(max_length=8, default="Inactive", choices=choices)
    product_image = models.ImageField(upload_to='products', null=False, blank=False)
    class Meta:
        abstract = False
    def __str__(self):
        return self.product_name