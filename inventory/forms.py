from django.forms import ModelForm
from .models import Products

class CRUDProductForm(ModelForm):
    class Meta:
        model = Products
        exclude = ['product_owner']