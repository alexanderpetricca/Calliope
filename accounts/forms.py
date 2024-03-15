from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


# Admin Forms

class CustomUserAdminCreateeForm(UserCreationForm):
    """Form used to create a user in the admin backend"""

    class Meta:
        model = CustomUser
        fields = ('__all__')


class CustomUserAdminChangeForm(UserChangeForm):
    """Form used to update a user in the admin backend"""

    class Meta:
        model = CustomUser
        fields = ('__all__')


# Front End Forms

class CustomUserChangeForm(forms.ModelForm):
    """Form used to allow user to update their details in the frontend"""

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
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
            'email': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Surname',
            }