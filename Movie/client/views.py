from django.shortcuts import render
from recommendation.models import Client

from django.contrib.auth.decorators import login_required

from login_signup.decorators import admin_required, client_required

# Create your views here.
@login_required
@client_required
def clienthome(request):
    count = Client.objects.filter(user=request.user).count()
    rated_movies = Client.objects.filter(user=request.user)
    context = {'count': count, 'rated_movies': rated_movies}
    return render(request, 'client/clienthome.html', context)
