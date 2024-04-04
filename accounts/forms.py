from django.contrib.auth import forms as auth_forms
from django import forms

from .models import CustomUser


# Admin Forms

class CustomUserAdminCreateForm(auth_forms.UserCreationForm):
    """Form used to create a user in the admin backend"""

    class Meta:
        model = CustomUser
        fields = ('__all__')


class CustomUserAdminChangeForm(auth_forms.UserChangeForm):
    """Form used to update a user in the admin backend"""

    class Meta:
        model = CustomUser
        fields = ('__all__')


# Custom Auth Forms
        
class CustomLoginForm(auth_forms.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class CustomSignupForm(auth_forms.UserCreationForm):

    first_name = forms.CharField(
        max_length=30, 
        label='First Name', 
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
    )
    
    last_name = forms.CharField(
        max_length=30, 
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
    )


    class Meta:
        model = CustomUser
        fields = (
            'username', 
            'first_name', 
            'last_name'
        )


    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password (again)'


class CustomPasswordResetForm(auth_forms.PasswordResetForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))


class CustomSetPasswordForm(auth_forms.SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'placeholder': 'New Password'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'})


class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'Old Password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'New Password (again)'


class CustomUserChangeForm(forms.ModelForm):
    """Form used to allow user to update their details in the frontend"""

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name', 
            'last_name',
        )

        labels = {
            'Email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Surname',
        }