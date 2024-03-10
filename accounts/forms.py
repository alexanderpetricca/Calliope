from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

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

class CustomUserChangeForm(ModelForm):
    """Form used to allow user to update their details in the frontend"""

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