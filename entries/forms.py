from django import forms

from .models import EntryMessage


class EntryMessageCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EntryMessageCreateForm, self).__init__(*args, **kwargs)
        
        body = self.fields['body']
        body.required = True
        body.widget = forms.Textarea(
            attrs={
                'placeholder': "Thoughts, Feelings & Ideas", 
                'rows': "1",
            }
        )

    class Meta:
        model = EntryMessage
        fields = ('body',)