from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from learners.models import LearnerProfile

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            LearnerProfile.objects.create(user=user, career_goal='Backend Developer')
            login(request, user)
            messages.success(request, f"Welcome to Career PathFinder, {user.first_name or user.username}!")
            return redirect('onboarding_start')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if not user and '@' in username:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username/email or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('landing')

def demo_login_view(request):
    # Quick 1-click Demo Login
    demo_user = User.objects.filter(username='demo').first()
    if not demo_user:
        demo_user = User.objects.create_user(
            username='demo',
            email='demo@careerpathfinder.ai',
            password='demo12345',
            first_name='Alex',
            last_name='Sharma'
        )
    # Ensure profile and seed
    login(request, demo_user)
    messages.success(request, "Logged in as Demo User (Alex Sharma - Java Backend Track)!")
    return redirect('dashboard')
