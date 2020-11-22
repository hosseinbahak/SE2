from django.db import models

class Movie(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    budget = models.PositiveIntegerField()
    genres = models.TextField()
    language = models.CharField(max_length=2)
    overview = models.TextField()
    companies = models.TextField()
    countries = models.TextField()
    release_date = models.DateField()
    revenue = models.PositiveIntegerField()
    runtime = models.FloatField()
    vote_average = models.FloatField()
    vote_count = models.PositiveIntegerField()
    casts = models.ManyToManyField('Cast')
    directors = models.ManyToManyField('Director')

class Cast(models.Model):
    SEX_CHOICES = [(0,'Male'), (1,'Female')]
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=70)
    gender = models.BooleanField(choices=SEX_CHOICES)
    movie_id = models.PositiveIntegerField()

class Director(models.Model):
    SEX_CHOICES = [(0,'Male'), (1,'Female')]
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=70)
    gender = models.BooleanField(choices=SEX_CHOICES)
    movie_id = models.PositiveIntegerField()
