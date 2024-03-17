from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash

from . import forms


def customLoginPageView(request):
    """
    Uses a custom login form that inherits the default Authentication form to give more creative control. Renders
    the login form on GET, and on POST processes the form and attempts to log the user in.
    """
    
    form = forms.CustomLoginForm(request)

    if request.user.is_authenticated:
        return redirect(reverse('entries_app_home'))

    if request.method == 'POST':
        form = forms.CustomLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else reverse('entries_app_home'))
        
    context = {
        'form': form,
    }
    return render(request, 'registration/login.html', context)


@login_required
def customLogoutPageView(request):
    """Logs the user out."""

    logout(request)
    return redirect(reverse('login'))


def customSignupView(request):
    
    form = forms.CustomSignupForm()

    if request.method == 'POST':

        form = forms.CustomSignupForm(request.POST)

        if form.is_valid():
            user = form.save(request)
            login(request, user)
            return redirect(reverse('login'))
        
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)


@login_required
def customPasswordChangeView(request):
    
    form = forms.CustomPasswordChangeForm(request.user)

    if request.method == 'POST':
        form = forms.CustomPasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('password_change_done'))
        
    context = {
        'form': form,
    }
    return render(request, 'registration/password_change.html', context)


def customPasswordChangeDoneView(request):
    return render(request, "registration/password_change_done.html")


@login_required
def userProfileView(request):
    """Renders the profile management page."""
    return render(request, 'accounts/profile.html')


@login_required
def updateUserProfileView(request):

    form = forms.CustomUserChangeForm(instance=request.user)

    if request.method == 'POST':
        form = forms.CustomUserChangeForm(request.POST)

        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }
    return render(request, 'accounts/updateprofile.html', context)
