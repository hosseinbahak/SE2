from rest_framework import serializers
from .models import Actor


class ActorsSerializer(serializers.Serializer):
    actor_id = serializers.IntegerField()
    name = serializers.CharField(max_length=70)
    gender = serializers.CharField(max_length=1)
    pic = serializers.CharField(max_length=50)
    movie_ids = serializers.CharField()


class GenresSerializer(serializers.Serializer):
    name = serializers.CharField()
    movie_ids = serializers.ListField()
    url = serializers.URLField()


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    casts = serializers.CharField(max_length=200)
    writers = serializers.CharField(max_length=200)
    directors = serializers.CharField(max_length=200)
    budget = serializers.IntegerField()
    genres = serializers.CharField(max_length=50)
    language = serializers.CharField(max_length=2)
    overview = serializers.CharField(max_length=200)
    companies = serializers.CharField(max_length=70)
    countries = serializers.CharField(max_length=70)
    release_date = serializers.DateField()
    revenue = serializers.IntegerField()
    runtime = serializers.FloatField()
    vote_average = serializers.FloatField()
    vote_count = serializers.IntegerField()
    poster = serializers.CharField(max_length=50)


class MoviesSerializer(serializers.Serializer):
    movie_ids = serializers.ListField()


class SearchSerializer(serializers.Serializer):
    movie_ids = serializers.ListField()
    acotr_ids = serializers.ListField()
    director_ids = serializers.ListField()
    writers_ids = serializers.ListField()
