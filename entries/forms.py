from django import forms

from .models import Entry


class EntryCreateUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Entry
        fields = ('content',)