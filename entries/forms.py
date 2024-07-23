from django import forms

from .models import Entry


class EntryCreateUpdateForm(forms.ModelForm):
    
    content = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'rows': '1',
            'autofocus': True,
            'placeholder': 'thoughts, feelings and ideas'
        },
    ))

    class Meta:
        model = Entry
        fields = ('content',)