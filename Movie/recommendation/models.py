from django.db import models
from login_signup.models import User
from django.core.validators import MaxValueValidator, MinValueValidator




# Models here ...


class Movie(models.Model):

    GENRE = (
        ('Action', 'Action'),
        ('Animation', 'Animation'),
        ('Comedy', 'Comedy'),
        ('Crime', 'Crime'),
        ('Horror', 'Horror'),
        ('Sci-Fi', 'Sci-Fi'),
        ('War', 'War'),
        ('Action Sci-Fi', 'Action Sci-Fi'),
        ('Comedy Crime', 'Comedy Crime'),
        ('Drama Thriller', 'Drama Thriller'),
    )

    YEAR = (
        (2010, '2010'), (2011, '2011'), (2012, '2012'), (2013, '2013'), (2014, '2014'), (2015, '2015'), (2016, '2016'), (2017, '2017'), (2018, '2018'), (2019, '2019'), (2020, '2020'), (2021, '2021'))

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, choices=GENRE)
    poster = models.FileField()
    imdbrating = models.FloatField(default=1.0)
    year = models.IntegerField(null=True, choices=YEAR)

    def __str__(self):
        return self.title


class Client(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='client_user')
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE, related_name="client_movie")
    rating = models.FloatField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return self.user.username
