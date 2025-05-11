from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FireAlert, DeviceStatus, TeamMember, ChatMessage, EmergencyContact, DeviceLog, AlertLog

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_admin', 'is_fire_team')
    list_filter = ('is_staff', 'is_active', 'is_admin', 'is_fire_team')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    # Add custom fields to the fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Roles', {'fields': ('is_admin', 'is_fire_team', 'location', 'status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Add custom fields to the add_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_admin', 'is_fire_team', 'location', 'status'),
        }),
    )

@admin.register(FireAlert)
class FireAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'status', 'timestamp', 'created_by')
    list_filter = ('status', 'timestamp', 'created_by')
    search_fields = ('title', 'location', 'description')
    ordering = ('-timestamp',)

@admin.register(DeviceStatus)
class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type', 'status', 'location', 'last_checked')
    list_filter = ('device_type', 'status', 'last_checked')
    search_fields = ('name', 'location', 'notes')
    ordering = ('-last_checked',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'last_location_update')
    list_filter = ('status', 'last_location_update')
    search_fields = ('user__username', 'user__email', 'equipment')
    ordering = ('-last_location_update',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'timestamp', 'is_read')
    list_filter = ('timestamp', 'is_read', 'sender', 'receiver')
    search_fields = ('message', 'sender__username', 'receiver__username')
    ordering = ('-timestamp',)

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('contact_type', 'name', 'phone_number', 'email')
    list_filter = ('contact_type',)
    search_fields = ('name', 'phone_number', 'email', 'address')
    ordering = ('contact_type', 'name')

@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ('device', 'action', 'performed_by', 'timestamp')
    list_filter = ('action', 'timestamp', 'performed_by')
    search_fields = ('device__name', 'action', 'notes')
    ordering = ('-timestamp',)

@admin.register(AlertLog)
class AlertLogAdmin(admin.ModelAdmin):
    list_display = ('alert', 'action', 'performed_by', 'timestamp')
    list_filter = ('action', 'timestamp', 'performed_by')
    search_fields = ('alert__title', 'action', 'notes')
    ordering = ('-timestamp',)
