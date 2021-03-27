from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
    path('update-cart/<int:pk>', views.update_cart, name="update-cart"),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
