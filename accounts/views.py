from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # If the user is an admin (or staff) redirect to Django admin, else to the home page.
            if user.is_staff or user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, "accounts/home.html")
