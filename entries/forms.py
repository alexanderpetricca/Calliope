from django import forms
from django.utils import timezone

from .models import Entry


class EntryCreateForm(forms.ModelForm):
    """Form used to create a new journal entry"""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EntryCreateForm, self).__init__(*args, **kwargs)
        
        body = self.fields['body']
        body.required = True
        body.widget = forms.Textarea(
            attrs={
                'placeholder': "Thoughts, Feelings & Ideas", 
                'rows': "3",
                'oninput': "autoResize(this)",
            }
        )


    class Meta:
        model = Entry
        fields = (
            'body',
        )

        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.author = self.user
            # instance.updated = timezone.now()        
        if commit:
            instance.save()
                    
        return instance


class EntryUpdateForm(EntryCreateForm):
    """Form used to update a journal entry"""