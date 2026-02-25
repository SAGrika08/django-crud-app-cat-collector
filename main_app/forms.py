from django import forms
from .models import Feeding

class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']

        widgets= {
            'date': forms.DateInput(
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            )
        }