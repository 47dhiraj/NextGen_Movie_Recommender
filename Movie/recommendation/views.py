from django.contrib import messages  
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import json                          
from django.http import Http404, HttpResponseForbidden
from .models import *
from login_signup.forms import CreateClientForm, CreateAdminForm, ImageUploadForm
from recommendation.models import User
from recommendation.models import Movie
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import MovieFilter
from django.core.cache import cache
import pandas as pd
import numpy as np
import sweetify
from .forms import RatingForm
from django.http import JsonResponse
import feather
import time
from django.views.decorators.cache import cache_page




## All views here ...


def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = User.objects.get(id=request.user.id)
            m.image = form.cleaned_data['image']
            m.save()
            if request.user.is_admin:
                return redirect('adminhome')
            else:
                return redirect('clienthome')
    return HttpResponseForbidden('Choose the photo first. Allowed only via POST')





def filtermovie(request):

    genre = request.POST.get('genre')
    year = request.POST.get('year')
    imdb_rating = request.POST.get('imdbrating')


    if request.method == 'POST':

        if genre == '' and year == '' and imdb_rating == '':

            myFilter = MovieFilter()
            return render(request, 'recommendation/filtermovies.html', {'myFilter': myFilter})


        movies_all = Movie.objects.all()


        myFilter = MovieFilter(request.POST, queryset=movies_all)

        movies_all = myFilter.qs

        page = request.GET.get('page', 1)
        paginator = Paginator(movies_all, 108)
        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            movies = paginator.page(paginator.num_pages)

        context = {'movies': movies, 'myFilter': myFilter}
        return render(request, 'recommendation/filtermovies.html', context)


    myFilter = MovieFilter()
    return render(request, 'recommendation/filtermovies.html', {'myFilter': myFilter})



def rate_movie(request, movie_id):

    if request.method == "POST":
        rating = request.POST.get('rating')
        try:
            clientObject = Client.objects.get(Q(user_id=request.user.id) & Q(movie_id=movie_id))
            form = RatingForm(request.POST or None, instance=clientObject)

            if rating != '0':
                edit = form.save(commit=False)
                edit.save()
                return JsonResponse({'status': 'true'}, status=200, safe=False)
        except:
            form = RatingForm(request.POST)
            if rating != '0':
                form.save()
                return JsonResponse({'status':'true'}, status=200,  safe=False)


        return JsonResponse({'status':'false'}, status=400,  safe=False)





@cache_page(360 * 2)
def detail(request,  movie_id, user_id=None):
    movies = get_object_or_404(Movie, id=movie_id)


    year = movies.year
    genre = movies.genre
    title = movies.title
    rate = 5
    movies_list = engine(title, rate)  


    recommended_movies = list()


    try:
        for i in range(len(movies_list)):
            try:
                queryset_movie = Movie.objects.filter(Q(title=movies_list[i])) 
                recommended_movies += queryset_movie  

                if len(recommended_movies) >= 6:
                    break

            except:
                continue

        context = {'movies': movies, 'recommended_movies': recommended_movies}
        return render(request, 'recommendation/detail.html', context)


    except:


        context = {'movies': movies, 'recommended_movies': recommended_movies}
        return render(request, 'recommendation/detail.html', context)





def engine(title, rate):

    name = []
    rating = []

    name.append(title)
    rating.append(rate)

    item_similarity_df = cache.get('cleaned_data')

    if item_similarity_df is None:
        item_similarity_df = feather.read_dataframe('item_similarity_df.feather')
        item_similarity_df.index = item_similarity_df.columns
        cache.set('cleaned_data', item_similarity_df, timeout=36000)


    movielist = []

    try:

        def get_similar_movies(movie_name, user_rating):

            user_rating = float(user_rating)  

            similar_score = item_similarity_df[movie_name] * (user_rating - 2.5)
            similar_score = similar_score.sort_values(ascending=False)

            return similar_score 

        def check_seen(movie, seen_movies):
            for item in seen_movies:
                if item == movie:
                    return True

            return False

        similar_movies = pd.DataFrame()  

        length = len(name)

        for i in range(0, length):
            similar_movies = similar_movies.append(get_similar_movies(name[i], rating[i]), ignore_index=True)
        all_recommend = similar_movies.sum().sort_values(ascending=False)



        i = 0
        for movie, score in all_recommend.iteritems():
            if not check_seen(movie, name):
                movielist.append(movie)

            i = i + 1
            if i >= 36 + length:
                break

        return movielist


    except:

        return movielist






@login_required
def suggestion(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    
    clients = Client.objects.filter(Q(user=request.user)).filter(Q(rating__gte=0.1)).order_by('-id')[:10]  

    movie_id = []
    title = []
    rate = []
    genre = []
    year = []

    suggested_movies = list()

    try:
        for client in clients:
            movie_id.append(client.movie_id)
            title.append(client.movie.title)
            rate.append(client.rating)
            genre.append(client.movie.genre)
            year.append(client.movie.year)

        movies_list = myengine(movie_id, title, rate, genre, year)



        for i in range(len(movies_list)):
            queryset_movie_suggestion = Movie.objects.filter(Q(title=movies_list[i]))
            suggested_movies += queryset_movie_suggestion

    except:
        pass

    context = {'suggested_movies': suggested_movies}
    return render(request, 'recommendation/suggestion.html', context)






def myengine(movie_id, name, rating, genre, year):

    item_similarity_df = cache.get('cleaned_data')

    if item_similarity_df is None:
        item_similarity_df = feather.read_dataframe('item_similarity_df.feather')
        item_similarity_df.index = item_similarity_df.columns
        cache.set('cleaned_data', item_similarity_df, timeout=36000)


    movielist = []

    temp_movie_id = []
    temp_movie_name = []
    temp_movie_genre = []
    temp_movie_year = []


    try:

        def get_similar_movies(movie_name, user_rating):  
            user_rating = float(user_rating)
            similar_score = item_similarity_df[movie_name] * (user_rating - 2.5) 
            similar_score = similar_score.sort_values(ascending=False)

            return similar_score  


        def check_seen(movie, seen_movies):
            for item in seen_movies:
                if item == movie:
                    return True

            return False


        length = len(name)

        cold_recommended_movies = []

        all_movies = Movie.objects.all()

        all_movies_list = []

        for movie in all_movies:
            all_movies_list.append(movie.title)


        all_recommended_movies = []

        for i in range(0, length):

            try:
                temp_recommended_movie_list = []
                all_suggested_movies = get_similar_movies(name[i], rating[i])
                temp_recommended_movie_list = list(all_suggested_movies.index)


                if rating[i] == 5.0:
                    for j in range(1, len(temp_recommended_movie_list)):
                        if temp_recommended_movie_list[j] in all_movies_list:
                            all_recommended_movies.append(temp_recommended_movie_list[j])

                        if len(all_recommended_movies) >= 6 * (i+1):
                            break


                elif rating[i] == 4.0:
                    count = 0
                    for j in range(len(temp_recommended_movie_list)):

                        if temp_recommended_movie_list[j] in all_movies_list:
                            count +=1
                            if count >= 8:
                                all_recommended_movies.append(temp_recommended_movie_list[j])

                        if len(all_recommended_movies) >= 6 * (i + 1):
                            break


                elif rating[i] == 3.0:
                    count = 0
                    for j in range(len(temp_recommended_movie_list)):

                        if temp_recommended_movie_list[j] in all_movies_list:
                            count += 1
                            if count >= 14:
                                all_recommended_movies.append(temp_recommended_movie_list[j])

                        if len(all_recommended_movies) >= 6 * (i + 1):
                            break


                elif rating[i] == 2.0:
                    count = 0
                    for j in range(len(temp_recommended_movie_list)):

                        if temp_recommended_movie_list[j] in all_movies_list:
                            count += 1
                            if count >= 7:
                                all_recommended_movies.append(temp_recommended_movie_list[j])

                        if len(all_recommended_movies) >= 6 * (i + 1):
                            break


                elif rating[i] == 1.0:
                    for j in range(0, len(temp_recommended_movie_list)):
                        if temp_recommended_movie_list[j] in all_movies_list:
                            all_recommended_movies.append(temp_recommended_movie_list[j])

                        if len(all_recommended_movies) >= 6 * (i+1):
                            break

            except:

                pass


        merged_recommended_movies = all_recommended_movies + cold_recommended_movies

        unique_merged_movies = []

        for x in merged_recommended_movies:
            if x not in unique_merged_movies:
                unique_merged_movies.append(x)



        i = 0
        for movie in unique_merged_movies:
            if not check_seen(movie, name):
                movielist.append(movie)

            i = i + 1
            if i >= 100 + length:
                break

        return movielist


    except:
        
        return movielist
