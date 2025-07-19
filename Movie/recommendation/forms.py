from django import forms
from .models import Client


class RatingForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['user', 'movie', 'rating']
