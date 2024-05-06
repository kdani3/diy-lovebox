# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout




@login_required
def profile(request):
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and 'upload' in request.POST:
        return redirect('image_handling:upload')
    if request.method == 'POST' and 'send' in request.POST:
        return redirect('image_handling:send')
    if request.method == 'POST' and 'cats' in request.POST:
        return redirect('cats:cats')
    if request.method == 'POST' and 'dogs' in request.POST:
        return redirect('dogs:dogs')
    return render(request, 'accounts/profile.html')
