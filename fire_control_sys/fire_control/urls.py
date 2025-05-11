from django.urls import path
from . import views

app_name = 'fire_control'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    
    # Dashboard URL
    path('', views.dashboard, name='dashboard'),
    
    # User Profile URLs
    path('profile/', views.user_profile, name='user_profile'),
    path('settings/', views.settings, name='settings'),
    
    # Fire Alert URLs
    path('alerts/', views.FireAlertListView.as_view(), name='fire_alerts'),
    path('alerts/create/', views.FireAlertCreateView.as_view(), name='fire_alert_create'),
    path('alerts/<int:pk>/', views.FireAlertDetailView.as_view(), name='fire_alert_detail'),
    path('alerts/<int:pk>/edit/', views.FireAlertUpdateView.as_view(), name='fire_alert_edit'),
    path('alerts/<int:pk>/delete/', views.FireAlertDeleteView.as_view(), name='fire_alert_delete'),
    path('alerts/<int:pk>/delete-ajax/', views.delete_fire_alert, name='fire_alert_delete_ajax'),
    
    # Device Status URLs
    path('devices/', views.DeviceStatusListView.as_view(), name='device_status'),
    path('devices/<int:pk>/update/', views.update_device_status, name='update_device_status'),
    
    # Team Management URLs
    path('team/', views.TeamMemberListView.as_view(), name='team_status'),
    path('team/create/', views.TeamMemberCreateView.as_view(), name='team_member_create'),
    path('team/<int:pk>/update/', views.TeamMemberUpdateView.as_view(), name='team_member_update'),
    path('team/<int:pk>/delete/', views.TeamMemberDeleteView.as_view(), name='team_member_delete'),
    
    # Chat URL
    path('chat/', views.chat, name='chat'),
    
    # Emergency Contact URL
    path('emergency/', views.emergency_contact, name='emergency_contact'),
]

