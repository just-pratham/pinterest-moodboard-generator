from django import forms
from .models import Moodboard

class MoodboardForm(forms.ModelForm):
    class Meta:
        model=Moodboard
        fields = ['title', 'description', 'background_color']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Give your Moodboard a name'
            }),
            'description':forms.TextInput(attrs={
                'placeholder': 'Describe your Moodboard',
                'rows':4
            }),
            'background_color': forms.TextInput(attrs={
                'type': 'color'
            }),
        }