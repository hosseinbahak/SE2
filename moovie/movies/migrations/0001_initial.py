# Generated by Django 3.1.3 on 2020-11-22 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('gender', models.BooleanField(choices=[(0, 'Male'), (1, 'Female')])),
                ('movie_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('gender', models.BooleanField(choices=[(0, 'Male'), (1, 'Female')])),
                ('movie_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('budget', models.PositiveIntegerField()),
                ('genres', models.TextField()),
                ('language', models.CharField(max_length=2)),
                ('overview', models.TextField()),
                ('companies', models.TextField()),
                ('countries', models.TextField()),
                ('release_date', models.DateField()),
                ('revenue', models.PositiveIntegerField()),
                ('runtime', models.FloatField()),
                ('vote_average', models.FloatField()),
                ('vote_count', models.PositiveIntegerField()),
                ('casts', models.ManyToManyField(to='movies.Cast')),
                ('directors', models.ManyToManyField(to='movies.Director')),
            ],
        ),
    ]
