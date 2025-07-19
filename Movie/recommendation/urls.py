from django.urls import path


from . import views

urlpatterns = [

    path('movies/', views.filtermovie, name='movies'),
    path('detail/<int:movie_id>/', views.detail, name='detail'),
    path('detail/<int:movie_id>/<int:user_id>/', views.detail, name='detail'),

    path('suggestion/', views.suggestion, name="suggestion"),
    path('upload_pic/', views.upload_pic, name="upload_pic"),

    path('rate_movie/<int:movie_id>/', views.rate_movie, name='rate_movie'),

]
