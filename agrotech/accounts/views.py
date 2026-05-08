"""
Accounts Views
- Register, Login, Logout, Profile, KYC Upload
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import RegisterForm, LoginForm, KYCUploadForm, ProfileEditForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome to AgroTech, {user.first_name or user.username}!")
        profile = user.profile
        if profile.role == 'farmer':
            return redirect('farmers:dashboard')
        return redirect('buyers:home')

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            profile = getattr(user, 'profile', None)
            if profile and profile.is_blocked:
                messages.error(request, "Your account has been blocked. Contact support.")
                return redirect('accounts:login')
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            if user.is_superuser:
                return redirect('admin_panel:dashboard')
            if profile and profile.role == 'farmer':
                return redirect('farmers:dashboard')
            return redirect('buyers:home')
        else:
            messages.error(request, "Invalid email or password.")

    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def edit_profile_view(request):
    profile = request.user.profile
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def kyc_upload_view(request):
    profile = request.user.profile

    if profile.kyc_status == 'approved':
        messages.info(request, "Your KYC is already approved.")
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = KYCUploadForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.kyc_status = 'pending'
            kyc.kyc_submitted_on = timezone.now()
            kyc.save()
            messages.success(request, "KYC submitted! We'll review it within 24–48 hours.")
            return redirect('accounts:profile')
    else:
        form = KYCUploadForm(instance=profile)

    return render(request, 'accounts/kyc_upload.html', {'form': form, 'profile': profile})


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        from .models import User
        try:
            user = User.objects.get(email=email)
            messages.success(request, "Password reset link sent to your email (check console in dev mode).")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
        return redirect('accounts:forgot_password')

    return render(request, 'accounts/forgot_password.html')
