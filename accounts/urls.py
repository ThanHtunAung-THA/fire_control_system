from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('support_home/', views.support_home_view, name='support_home'),
    path('team_home/', views.team_home_view, name='team_home'),
    path('manage.db/', views.manage_db_view, name='manage_db'),
    path('superuser_dashboard/', views.superuser_dashboard, name='superuser_dashboard'),
] 