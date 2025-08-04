from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, Registration
from .forms import UserRegisterForm, EventRegistrationForm

def index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', {'events': events})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'events/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.event = event
            registration.save()
            # Send confirmation email
            try:
                send_mail(
                    'Event Registration Confirmation',
                    f'You have successfully registered for {event.title}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            return redirect('index')
    else:
        form = EventRegistrationForm()
    return render(request, 'events/event_detail.html', {'event': event, 'form': form})

@login_required
def my_registrations(request):
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    return render(request, 'events/my_registrations.html', {'registrations': registrations})

@login_required
def cancel_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        registration.delete()
        return redirect('my_registrations')
    return render(request, 'events/cancel_registration.html', {'registration': registration})
