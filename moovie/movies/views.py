from django.http import Http404, HttpResponseServerError
from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder, loads
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from random import randint
from .models import *
from .serializers import *
import json


def home(request):
    data = top_rated(request)
    top_rated_data_raw = json.loads(data.rendered_content.decode('utf8'))
    top_rated_data = []
    for movie in top_rated_data_raw['movie_ids'][:10]:
        data = movie_details(request, movie)
        top_rated_data.append(json.loads(data.rendered_content.decode('utf8')))

    data = release_date(request)
    release_date_data_raw = json.loads(data.rendered_content.decode('utf8'))
    release_date_data = []
    for movie in release_date_data_raw['movie_ids'][:5]:
        data = movie_details(request, movie)
        release_date_data.append(json.loads(data.rendered_content.decode('utf8')))

    data = random(request)
    random_data_raw = json.loads(data.rendered_content.decode('utf8'))
    random_data = []
    for movie in random_data_raw['movie_ids'][:5]:
        data = movie_details(request, movie)
        random_data.append(json.loads(data.rendered_content.decode('utf8')))

    context = {'top_rated': top_rated_data, 'top_release': release_date_data, 'random': random_data}
    return render(request, 'index.html', context=context)


def check_DB():
    if Movie.objects.exists() and Actor.objects.exists() and Director.objects.exists() and Writer.objects.exists():
        return True
    else:
        return False


@api_view(['GET'])
def all_actors(request, actor_id):
    # returns only one Actor
    if actor_id:
        # if the actor_id is valid
        try:
            data = Actor.objects.get(actor_id=actor_id)
            result = ActorsSerializer(data).data
            return Response(result)
        except Actor.DoesNotExist:
            raise Http404('actor not found')
    # returns all the Actors
    else:
        # if data base is not loaded then return 500 Error
        if not check_DB():
            return HttpResponseServerError('Database is not loaded !')
        data = Actor.objects.all()
        result = ActorsSerializer(data, many=True).data
        # add url to each Actor
        for actor in result:
            # reverse create full link to each actor
            actor['url'] = reverse('all_actors', args=[
                                str(actor['actor_id'])], request=request)
        return Response(result)


@api_view(['GET'])
def all_genres(request, which_genre):
    if not which_genre:
        # if data base is not loaded then return 500 Error
        if not check_DB():
            return HttpResponseServerError('Database is not loaded !')
        # returns all genres
        movies = Movie.objects.all()
        data = []
        for movie in movies:
            for genre in movie.genres.split(','):
                for available_genre in data:
                    # if we had the genre before just add the movie id
                    if available_genre['name'] == genre:
                        available_genre['movie_ids'].append(movie.id)
                        break
                else:
                    # if we don't have that genre create a new one
                    dic = {'name': genre, 'movie_ids': [movie.id], 'url': reverse(
                        'all_genres', args=[genre], request=request)}
                    data.append(dic)
        result = GenresSerializer(data, many=True).data
        return Response(result)
    else:
        # return only one genre
        movies = Movie.objects.all()
        data = {'name': which_genre, 'movie_ids': [], 'url': reverse(
            'all_genres', args=[which_genre], request=request)}
        # if which_genre is valid then: flag_which_genre == True
        flag_which_genre = False
        # search for which_genre
        for movie in movies:
            for genre in movie.genres.split(','):
                if genre == which_genre:
                    # if genre is valid then add movie_id to the list
                    data['movie_ids'].append(movie.id)
                    flag_which_genre = True
        if flag_which_genre == True:
            result = GenresSerializer(data).data
            return Response(result)
        else:
            raise Http404('genre not found')


@api_view(['GET'])
def movie_details(request, movie_id):
    casts = Actor.objects.all()
    directors = Director.objects.all()
    writers = Writer.objects.all()
    movie_genres = []
    casts_name = []
    writers_name = []
    directors_name = []

    try:
        movie_info = Movie.objects.filter(id=movie_id).get()
        movie_poster_url = "https://image.tmdb.org/t/p/original" + movie_info.poster

        for genre in movie_info.genres.split(','):
                movie_genres.append(genre)


        for cast in casts:
            for castMovieId in cast.movie_ids.split(','):
                if int(castMovieId) == movie_id:
                    casts_name.append(cast.name)

        for writer in writers:
            for writers_movie_ids in writer.movie_ids.split(','):
                if int(writers_movie_ids) == movie_id:
                    writers_name.append(writer.name)

        for director in directors:
            for directorMovieId in director.movie_ids.split(','):
                if int(directorMovieId) == movie_id:
                    directors_name.append(director.name)

        data = {
            'id': movie_id,
            'title': movie_info.title,
            'casts': casts_name,
            'writers': writers_name,
            'directors': directors_name,
            'budget': movie_info.budget,
            'genres': movie_genres,
            'language': movie_info.language,
            'overview': movie_info.overview,
            'companies': movie_info.companies,
            'countries': movie_info.countries,
            'release_date': movie_info.release_date,
            'revenue': movie_info.revenue,
            'runtime': movie_info.runtime,
            'vote_average': movie_info.vote_average,
            'vote_count': movie_info.vote_count,
            'poster': movie_poster_url
        }
        data = MovieSerializer(data).data
        return Response(data)

    except:
        return JsonResponse({
            'status': 0,
        }, encoder=JSONEncoder)


@api_view(['GET'])
# it gets top 20 movies that have most rate
def top_rated(request):
    movie_info = Movie.objects.order_by('-vote_average').values('id')[:20]
    data = {'movie_ids': []}
    for movie in movie_info:
        data['movie_ids'].append(movie['id'])
    data = MoviesSerializer(data).data
    return Response(data)


@api_view(['GET'])
# it gets top 20 movies sorted by last release
def release_date(request):
    movie_info = Movie.objects.order_by('-release_date').values('id')[:20]
    data = {'movie_ids': []}
    for movie in movie_info:
        data['movie_ids'].append(movie['id'])
    data = MoviesSerializer(data).data
    return Response(data)


@api_view(['GET'])
def random(request):
    # if data base is not loaded then return 500 Error
    if not check_DB():
        return HttpResponseServerError('Database is not loaded !')
    # how many random movies
    if 'num' in request.GET and request.GET['num'].isnumeric():
        NUMBERS = int(request.GET['num'])
    else:
        NUMBERS = 10
    # bring all ids from movies DB
    all_ids = Movie.objects.all().values('id')
    data = {'movie_ids': []}
    if len(all_ids) < NUMBERS:
        for item in all_ids:
            data['movie_ids'].append(item['id'])
    else:
        # select NUMBERS of them by random
        c = 0
        while c < NUMBERS:
            random_int = randint(0, len(all_ids) - 1)
            if all_ids[random_int]['id'] not in data['movie_ids']:
                data['movie_ids'].append(all_ids[random_int]['id'])
                c += 1
    result = MoviesSerializer(data).data
    return Response(result)


@api_view(['GET'])
def search(request):
    if not check_DB():
        return HttpResponseServerError('Database is not loaded !')
    we_found_something = True
    name = request.GET['search']
    queryset_movies = Movie.objects.filter(title__contains=name).values('id')
    queryset_actors = Actor.objects.filter(
        name__contains=name).values('actor_id')
    queryset_writers = Writer.objects.filter(
        name__contains=name).values('writer_id')
    queryset_director = Director.objects.filter(
        name__contains=name).values('director_id')
    # if nothing founds
    if queryset_movies.count() == 0 and queryset_actors.count() == 0 and queryset_writers.count() == 0 and queryset_director.count() == 0:
        we_found_something = False
    if we_found_something:
        data = {'movie_ids': queryset_movies, 'acotr_ids': queryset_actors,
                'director_ids': queryset_director, 'writers_ids': queryset_writers}
        result = SearchSerializer(data).data
        return Response(result)
    else:
        raise Http404("we couldn't find what you're looking for")
