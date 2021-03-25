from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as authviews

urlpatterns = [
    path('', views.register, name='register'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', authviews.LoginView.as_view(template_name='login.html'), name="login") ,
    path('logout/', authviews.LogoutView.as_view(template_name = 'logout.html'), name="logout"),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
