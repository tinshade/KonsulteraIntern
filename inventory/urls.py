from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
   path('listing/', views.listing, name='listing'),
   path('item_details/item/', views.crud_product, name="add_item"),
   path('item_details/item/<int:pk>', views.crud_product, {}, 'edit_item'),
   path('delete_item/<int:pk>', views.delete_item,{},'delete_item'),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
