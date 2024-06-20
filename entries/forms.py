from django import forms

from .models import EntryMessage


class EntryMessageCreateForm(forms.ModelForm):

    body = forms.CharField(
        widget = forms.Textarea(attrs={
            'placeholder': "Thoughts, Feelings & Ideas", 
            'rows': "1"
        }),
        max_length = 1000,
        error_messages = {
            'max_length': 'Please limit the text to 1000 characters or fewer.',
        }
    )

    class Meta:
        model = EntryMessage
        fields = ('body',)