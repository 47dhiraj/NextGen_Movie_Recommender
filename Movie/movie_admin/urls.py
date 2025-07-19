from django.urls import path

from . import views

urlpatterns = [

    path('adminhome/', views.adminhome, name="adminhome"),
    path('adminpanel/', views.adminpanel, name="adminpanel"),
    path('view_rating_details/<int:id>', views.rating_details, name="rating_details"),
    path('delete/<int:id>', views.delete, name="delete"),

    path('list_movies/', views.listMovies, name="list_movies"),
    path('add_movies/', views.addMovies, name="add_movies"),
    path('delete_movies/<int:movie_id>', views.deleteMovies, name="delete_movies"),
    path('edit_movies/<int:movie_id>', views.editMovies, name="edit_movies"),

    path('download_csv/', views.dwonloadCSV, name="download_csv")

]
