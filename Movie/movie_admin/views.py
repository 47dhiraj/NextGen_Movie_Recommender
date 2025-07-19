from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login_signup.decorators import admin_required, client_required
from login_signup.models import User
from recommendation.models import Client, Movie
from .forms import AddMoviesForm
import sweetify
import csv

# Create your views here.
@login_required
@admin_required
def adminhome(request):
    count = Client.objects.filter(user=request.user).count()
    movie_count = Movie.objects.all().count()
    user_count = User.objects.all().count()
    admin_count = User.objects.filter(is_admin=1).count()
    context = {'count': count, 'movie_count': movie_count, 'user_count': user_count, 'admin_count': admin_count}
    return render(request, 'movie_admin/adminhome.html', context)


@login_required
@admin_required
def adminpanel(request):
    users = User.objects.all()  # .objects le chai whole table ko records lai nai as object return garxa
    clients = Client.objects.all()
    context = {'users': users, 'clients': clients}
    return render(request, 'movie_admin/adminpanel.html', context)


@login_required
@admin_required
def rating_details(request, id):  # url request ma id pani aauxa as parameter to this edit function
    users = User.objects.get(
        id=id)  # id(primary key) ko help batw table ma vayeko pariticular user ko record set nikaleko
    clients = Client.objects.filter(
        user=id)  # Note :  FOREIGN KEY CONCEPT   # .Filter le table ma vayeko selective  records set lai retun gari rako hunxa  # parameter batw aayeko id lai, Client table ko user vanni foreigh key wala field(column)  ma assign garya ho because particular  id ko jati record tyo client ma cha sabbai chaiyeko vayera
    counts = Client.objects.filter(user=id).count()
    context = {'clients': clients, 'users': users, 'counts': counts}
    # print(counts)
    return render(request, 'movie_admin/rating_details.html', context)


@login_required
@admin_required
def delete(request, id):  # url request ma id pani aauxa as parameter to this delete function.
    users = User.objects.get(id=id)
    users.delete()
    return redirect('adminpanel')


@login_required
@admin_required
def listMovies(request):
    all_movies = Movie.objects.all()
    context = {'all_movies': all_movies}
    return render(request, 'movie_admin/list_movies.html', context)


@login_required
@admin_required
def addMovies(request):

    if request.method == 'POST':
        print(request)
        form = AddMoviesForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            try:
                form.save()
                sweetify.success(request, 'Movie added successfully!',
                                 text='Good job! You have successfully added Movie.',
                                 persistent='ok', icon='success')
            except Exception as e:
                sweetify.error(request, 'Something Went Wrong', text=str(e), persistent='Close', icon='error')
                return redirect('add_movies')

    form = AddMoviesForm()
    return render(request, 'movie_admin/add_movies.html', {'form': form})


@login_required
@admin_required
def deleteMovies(request, movie_id):
    if request.method == 'POST':
        delete_movie = Movie.objects.get(pk=movie_id)
        delete_movie.delete()
        sweetify.success(request, 'Movie deleted successfully!',
                         text='Good job! You have successfully deleted Movie.',
                         persistent='ok', icon='success')
        return redirect('list_movies')


def editMovies(request, movie_id):
    if request.method == 'POST':
        edit_record = Movie.objects.get(pk=movie_id)
        form = AddMoviesForm(request.POST or None, request.FILES or None, instance=edit_record)  # request.FILES is needed for updating the image field as well and while saving form we need to do this => edit = form.save(commit=False) and then only edit.save()
        if form.is_valid:
            edit = form.save(commit=False)
            edit.save()
            sweetify.success(request, 'Movie edited successfully!',
                             text='Good job! You have successfully edited Movie.',
                             persistent='ok', icon='success')

        return redirect('list_movies')
    else:
        edit_record = Movie.objects.get(pk=movie_id)
        form = AddMoviesForm(instance=edit_record)

    return render(request, 'movie_admin/edit_movies.html', {'form': form})



def dwonloadCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ratings.csv"'
    writer = csv.writer(response)

    writer.writerow(['userId', 'movieId', 'rating'])
    clients = Client.objects.all().values_list('user', 'movie', 'rating')
    for client in clients:
        writer.writerow(client)
    return response

