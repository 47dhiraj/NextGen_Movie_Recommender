from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name="adminpanel"),

    path('', include('recommendation.urls')),
    path('', include('home.urls')),
    path('', include('login_signup.urls')),
    path('', include('movie_admin.urls')),
    path('', include('client.urls')),


]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)