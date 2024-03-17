from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


# Admin Forms

class CustomUserAdminCreateForm(UserCreationForm):
    """Form used to create a user in the admin backend"""

    class Meta:
        model = CustomUser
        fields = ('__all__')


class CustomUserAdminChangeForm(UserChangeForm):
    """Form used to update a user in the admin backend"""

    class Meta:
        model = CustomUser
        fields = ('__all__')


# Frontend Forms
        
class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class CustomSignupForm(UserCreationForm):

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

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


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