from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_fire_team = models.BooleanField(default=False)
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=50, default='available')
    
    def __str__(self):
        return self.username

class FireAlert(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('contained', 'Contained'),
        ('extinguished', 'Extinguished'),
        ('false_alarm', 'False Alarm'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES, default='medium')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} - {self.status}"

class DeviceStatus(models.Model):
    DEVICE_TYPES = [
        ('sprinkler', 'Sprinkler'),
        ('extinguisher', 'Fire Extinguisher'),
        ('alarm', 'Fire Alarm'),
        ('water_tank', 'Water Tank'),
        ('door', 'Fire Door'),
        ('evacuation_route', 'Evacuation Route'),
        ('pump', 'Fire Pump'),
        ('water_sprayer', 'Water Sprayer'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
        ('faulty', 'Faulty'),
    ]
    
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    location = models.CharField(max_length=200)
    last_checked = models.DateTimeField(auto_now=True)
    last_maintained = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.device_type}"

class TeamMember(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('on_duty', 'On Duty'),
        ('responding', 'Responding'),
        ('off_duty', 'Off Duty'),
    ]
    
    ROLE_CHOICES = [
        ('firefighter', 'Firefighter'),
        ('firewatch', 'FireWatch'),
        ('team_leader', 'Team Leader'),
        ('equipment_manager', 'Equipment Manager'),
        ('safety_officer', 'Safety Officer'),
        ('paramedic', 'Paramedic'),
        ('driver', 'Driver'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available')
    equipment = models.TextField(blank=True)
    last_location_update = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name or self.user.username} - {self.role or 'No Role'}"

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

class EmergencyContact(models.Model):
    CONTACT_TYPES = [
        ('hospital', 'Hospital'),
        ('police', 'Police'),
        ('fire_department', 'Fire Department'),
        ('traffic_police', 'Traffic Police'),
        ('rescue_team', 'Rescue Team'),
    ]
    
    contact_type = models.CharField(max_length=50, choices=CONTACT_TYPES)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_contact_type_display()} - {self.name}"

class DeviceLog(models.Model):
    device = models.ForeignKey(DeviceStatus, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.device.name} - {self.action}"

class AlertLog(models.Model):
    alert = models.ForeignKey(FireAlert, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.alert.title} - {self.action}"

    