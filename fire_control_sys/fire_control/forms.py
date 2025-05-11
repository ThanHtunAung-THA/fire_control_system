from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, FireAlert, DeviceStatus, TeamMember

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_admin', 'is_fire_team')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_fire_team': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FireAlertForm(forms.ModelForm):
    class Meta:
        model = FireAlert
        fields = ('title', 'description', 'location', 'status', 'severity', 'notes')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DeviceControlForm(forms.ModelForm):
    class Meta:
        model = DeviceStatus
        fields = ('name', 'device_type', 'status')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ChatMessageForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Type your message...'
        })
    )

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ('name', 'role', 'contact_number', 'status', 'equipment')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'equipment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class EmergencyContactForm(forms.Form):
    CONTACT_CHOICES = [
        ('hospital', 'Hospital'),
        ('police', 'Police'),
        ('fire_department', 'Fire Department'),
        ('traffic_police', 'Traffic Police'),
        ('rescue_team', 'Rescue Team'),
    ]
    
    contact_type = forms.ChoiceField(
        choices=CONTACT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter emergency message...'
        })
    ) 