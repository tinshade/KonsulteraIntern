from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,ProfileRegisterForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model
User = get_user_model()
#REGISTRATION PAGE
def register(request):
    if request.user.is_authenticated:
        return redirect('listing')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            usertype = request.POST['usertype']
            user = form.save()
            Profile.objects.create (user=user,usertype=usertype)
            messages.success(request, f'Hey! Try logging in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
        'title':'Register | PYWarehouse'
    }
    return render(request, 'register.html', context)

@login_required
def profile(request):
    return render(request, 'landing.html', {'title': 'Profile'})

def add_product(request):
    context={
        "title":"Konsultera | Add Product"
    }
    return render(request, 'additem.html', context)