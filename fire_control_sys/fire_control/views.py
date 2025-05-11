from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth import login
from .models import User, FireAlert, DeviceStatus, TeamMember, ChatMessage
from .forms import (
    UserRegistrationForm, FireAlertForm, DeviceControlForm,
    ChatMessageForm, TeamMemberForm, EmergencyContactForm
)

# Authentication Views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('fire_control:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'fire_control/register.html', {'form': form})

# Dashboard View
@login_required
def dashboard(request):
    context = {
        'active_alerts_count': FireAlert.objects.filter(status='active').count(),
        'team_members_count': TeamMember.objects.count(),
        'active_devices_count': DeviceStatus.objects.filter(status='active').count(),
        'unread_messages_count': ChatMessage.objects.filter(
            receiver=request.user, is_read=False
        ).count(),
        'recent_alerts': FireAlert.objects.order_by('-timestamp')[:5],
        'team_status': TeamMember.objects.all(),
        'device_status': DeviceStatus.objects.all(),
    }
    return render(request, 'fire_control/dashboard.html', context)

# Fire Alert Views
class FireAlertListView(LoginRequiredMixin, ListView):
    model = FireAlert
    template_name = 'fire_control/fire_alerts.html'
    context_object_name = 'alerts'
    ordering = ['-timestamp']

class FireAlertCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FireAlert
    form_class = FireAlertForm
    template_name = 'fire_control/fire_alert_form.html'
    success_url = reverse_lazy('fire_control:fire_alerts')

    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_fire_team

class FireAlertDetailView(LoginRequiredMixin, DetailView):
    model = FireAlert
    template_name = 'fire_control/fire_alert_detail.html'

# Device Control Views
class DeviceStatusListView(LoginRequiredMixin, ListView):
    model = DeviceStatus
    template_name = 'fire_control/device_status.html'
    context_object_name = 'devices'

@login_required
def update_device_status(request, pk):
    if request.method == 'POST' and (request.user.is_admin or request.user.is_fire_team):
        device = get_object_or_404(DeviceStatus, pk=pk)
        form = DeviceControlForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Team Management Views
class TeamMemberListView(LoginRequiredMixin, ListView):
    model = TeamMember
    template_name = 'fire_control/team_status.html'
    context_object_name = 'team_members'

class TeamMemberCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'fire_control/team_member_form.html'
    success_url = reverse_lazy('fire_control:team_status')

    def test_func(self):
        return self.request.user.is_admin

    def form_valid(self, form):
        # Create a new user first
        user = User.objects.create_user(
            username=form.cleaned_data['name'].lower().replace(' ', '_'),
            email=f"{form.cleaned_data['name'].lower().replace(' ', '_')}@fireteam.com",
            password='changeme123',  # Default password that should be changed
            is_fire_team=True
        )
        
        # Create the team member with the user
        team_member = form.save(commit=False)
        team_member.user = user
        team_member.save()
        
        messages.success(self.request, f'Team member {team_member.name} created successfully. Default password is "changeme123"')
        return super().form_valid(form)

class TeamMemberUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'fire_control/team_member_form.html'
    success_url = reverse_lazy('fire_control:team_status')

    def test_func(self):
        return self.request.user.is_admin

class TeamMemberDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TeamMember
    template_name = 'fire_control/team_member_confirm_delete.html'
    success_url = reverse_lazy('fire_control:team_status')

    def test_func(self):
        return self.request.user.is_admin

# Chat Views
@login_required
def chat(request):
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return JsonResponse({'success': True})
    else:
        form = ChatMessageForm()
    
    messages = ChatMessage.objects.filter(
        sender=request.user
    ) | ChatMessage.objects.filter(
        receiver=request.user
    )
    messages = messages.order_by('timestamp')
    
    return render(request, 'fire_control/chat.html', {
        'form': form,
        'messages': messages
    })

# Emergency Contact View
@login_required
def emergency_contact(request):
    if request.method == 'POST' and (request.user.is_admin or request.user.is_fire_team):
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact_type = form.cleaned_data['contact_type']
            message = form.cleaned_data['message']
            # Here you would implement the actual emergency contact logic
            messages.success(request, f'Emergency message sent to {contact_type}!')
            return redirect('fire_control:dashboard')
    else:
        form = EmergencyContactForm()
    
    return render(request, 'fire_control/emergency_contact.html', {'form': form})

