from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from django.contrib.sites.models import Site

from .models import SignUpCode, EmailConfirmationToken
from . import forms
from core.utils import genericSendEmail


def custom_login_page_view(request):
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
            return redirect(request.GET['next'] if 'next' in request.GET else reverse('entries_entry_list'))
        
    context = {
        'form': form,
    }
    return render(request, 'registration/login.html', context)


@login_required
def custom_logout_page_view(request):
    """
    Logs the user out.
    """

    logout(request)
    return redirect(reverse('login'))


def custom_signup_view(request):

    if request.user.is_authenticated:
        return redirect('entries_app_home')
    
    form = forms.CustomSignupForm()

    if request.method == 'POST':

        form = forms.CustomSignupForm(request.POST)

        if form.is_valid():

            code = form.cleaned_data.get('signup_code')

            try:
                signup_code = SignUpCode.objects.get(code=code)
                if signup_code:
                    user = form.save(commit=False)
                    user.save()
                    signup_code.delete()
                    
                    login(request, user)
                    return redirect(reverse('entries_app_home'))
                
            except ObjectDoesNotExist:
                form.add_error('signup_code', 'This code is not valid.')
        
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)


@login_required
def custom_password_change_view(request):
    
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


@login_required
def custom_password_change_done_view(request):
    return render(request, "registration/password_change_done.html")


@login_required
def user_profile_view(request):
    """
    Renders the profile management page.
    """

    return render(request, 'accounts/profile.html')


@login_required
def update_user_profile_view(request):

    form = forms.CustomUserProfileChangeForm(instance=request.user)

    if request.method == 'POST':
        form = forms.CustomUserProfileChangeForm(request.POST)

        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }
    return render(request, 'accounts/update-profile.html', context)


@login_required
def update_user_email_view(request):

    form = forms.CustomUserEmailChangeForm()

    if request.method == 'POST':
        form = forms.CustomUserEmailChangeForm(request.POST)

        if form.is_valid():

            new_email = form.cleaned_data['email']

            token, created = EmailConfirmationToken.objects.get_or_create(
                user = request.user,
                email = new_email,
            )

            email_data = {
                'confirm_url': str(Site.objects.get_current()) + reverse('update_email_confirm', args=[token.id])
            }

            genericSendEmail(
                'registration/email/confirm-email-change.html',
                'Confirm Email Change',
                [new_email,],
                email_data,
                f'Send user email change confirmation: {str(request.user.id)}'
            )

            return redirect(reverse('update_email_sent'))

    context = {
        'form': form,
    }

    return render(request, 'accounts/update-email.html', context)


@login_required
def update_user_email_sent_view(request):
    
    return render(request, 'registration/email-token-sent.html')


@login_required
def update_user_email_confirm_view(request, pk):
    
    try:
        token = EmailConfirmationToken.objects.get(id=pk)
        if timezone.now() - token.created > timezone.timedelta(days=1):            
            token.delete()
            context = {
                'error_message': 'Confirmation Link Expired.',
            }
            return render(request, 'registration/email-confirmation-error.html', context)
        
        else:        
            user = token.user
            user.email = token.email
            user.email_confirmed = True
            user.save()
            token.delete()
            return redirect(reverse('update_email_success'))
    
    except (ObjectDoesNotExist, ValidationError):
        context = {
            'error_message': 'Invalid Confirmation Link'
        }
        return render(request, 'registration/email-confirmation-error.html', context)    


@login_required
def update_user_email_confirm_error(request):
    
    return render(request, 'registration/email-confirm-error.html') 


@login_required
def update_user_email_confirm_success(request):
    
    return render(request, 'registration/email-confirm-success.html')  

