from django.shortcuts import render, redirect

# Create your views here.
import json                           # yedi request ma json object aai rako cha vani.. so json data lai django view ma access garna ko lagi import json lekhna parcha
from django.http import JsonResponse  # Django ko view batw normally http response pathaine garincha but AJAX call ko scenario ma django batw AJAX call lai respone pathauda kheri json ko format ma respone pathauna parcha (i.e JsonResponse) so JsonRespone pathauna ko lagi yesari import garna parcha

from recommendation.models import Movie

from django.core.cache import cache
import pandas as pd
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request, movie_genre=None, imdb_rating=None, year=None, latest=None):

    if request.method == 'POST':
        query = json.loads(request.body).get('searchText')  # json object ma as a key value pair ma data aai rako huncha.. so teslai django ko dictionary ma laijana ko lagi json.loads() gareko
        movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
        data = movies.values()  # movies ma queryset huncha so tyo queryset batw  it returns Values of QuerySet object
        return JsonResponse(list(data),safe=False)  # list(data) convets values of Queryset object in python list... but but hamile json response ma khas list pathaune tw haina.. because ajax call is expecting json object so list pani pathauna milos vanera  safe=False ko use gareko ho

    query = request.GET.get('searchvalue')
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
        context = {'movies': movies}
        return render(request, 'home/index.html', context)

    # item_similarity_df = cache.get('cleaned_data')
    # if item_similarity_df is None:
    #     item_similarity_df = pd.read_csv('item_similarity_df.csv', index_col=0)
    #     cache.set('cleaned_data', item_similarity_df, timeout=36000)


    if movie_genre:
        if movie_genre == 'Action' or movie_genre == 'Animation' or movie_genre == 'Comedy' or movie_genre == 'Crime' or movie_genre == 'Horror' or movie_genre == 'Sci-Fi' or movie_genre == 'War' or movie_genre == 'Action Sci-Fi' or movie_genre == 'Comedy Crime' or movie_genre == 'Drama Thriller':
            movies_all = Movie.objects.filter(genre=movie_genre)
        else:
            return redirect('home')

    elif imdb_rating:
        movies_all = Movie.objects.filter(Q(imdbrating__gte=8.0))

    elif year:
        if year == 2016 or year == 2015 or year == 2014 or year == 2013 or year == 2012 or year == 2011:
            movies_all = Movie.objects.filter(year=year)
        else:
            return redirect('home')

    # elif latest:
    #     movies_all = Movie.objects.filter(Q(year__gte=2020))

    else:
        movies_all = Movie.objects.filter(year=2016)
    # print(movies_all)

    page = request.GET.get('page', 1)
    paginator = Paginator(movies_all, 12)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    context = {'movies': movies}
    return render(request, 'home/index.html', context)
