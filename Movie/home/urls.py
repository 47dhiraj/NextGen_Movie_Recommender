from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', csrf_exempt(views.home), name="home"), # yedi ajax call batw hamro view ma aauda csrf token pathaunu chaina vani , csrf_exempt lai import garna parcha.. ani csrf_exempt le hamro view lai surround pani garna parcha
    path('genre/<str:movie_genre>', views.home),
    path('toprating/<str:imdb_rating>', views.home),
    path('year/<int:year>', views.home),
    path('recent/<str:latest>', views.home),



]
