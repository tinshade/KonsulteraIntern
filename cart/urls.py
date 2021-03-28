from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.update_item, name="update_item"),
    path('get_items/', views.get_items, name="get_items"),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
