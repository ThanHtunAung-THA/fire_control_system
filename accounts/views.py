from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on user role
            if user.is_superuser:
                return redirect('superuser_dashboard')
            elif user.groups.filter(name='Fire Control Support').exists():
                return redirect('support_home')
            elif user.groups.filter(name='Fire Control Team').exists():
                return redirect('team_home')
            else:
                messages.error(request, "User does not belong to any group.")
                logout(request)
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def support_home_view(request):
    return render(request, "accounts/support_home.html")

@login_required
def team_home_view(request):
    return render(request, "accounts/team_home.html")

def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func

@superuser_required
def manage_db_view(request):
    # Add your database management logic here
    return render(request, "accounts/manage_db.html")

@login_required
def home_view(request):
    return render(request, "accounts/home.html")

@login_required
def superuser_dashboard(request):
    return render(request, "accounts/superuser_dashboard.html")
