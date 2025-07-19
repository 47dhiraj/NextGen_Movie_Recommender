from django import forms
from recommendation.models import Movie


class AddMoviesForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'genre', 'poster', 'imdbrating', 'year')
