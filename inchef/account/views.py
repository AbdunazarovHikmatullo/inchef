from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'account/auth/register.html', {
        'form': form
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'account/auth/login.html', {
        'form': form
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')




def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    products = profile_user.products.filter(is_active=True).select_related('category')
    
    return render(request, 'account/profile/profile.html', {
        'profile_user': profile_user,
        'products': products
    })