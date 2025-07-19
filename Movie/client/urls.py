from django.urls import path

from . import views

urlpatterns = [
    path('clienthome/', views.clienthome, name="clienthome"),
]
