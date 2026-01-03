from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm


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
    return render(request, 'account/profile/profile.html')