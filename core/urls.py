from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as authviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('inventory/', include('inventory.urls')),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
