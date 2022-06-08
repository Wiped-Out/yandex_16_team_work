import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class MovieType(models.TextChoices):
    MOVIE = 'MV', _('movie')
    TV_SHOW = 'TS', _('tv_show')


class PersonRoleType(models.TextChoices):
    DIRECTOR = 'director', _('director')
    ACTOR = 'actor', _('actor')
    WRITER = 'writer', _('writer')


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [models.UniqueConstraint(
            fields=['film_work', 'genre'],
            name='film_work_genre_idx')]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = "Человек"
        verbose_name_plural = "Люди"

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=PersonRoleType.choices)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [models.UniqueConstraint(
            fields=['film_work', 'person', 'role'],
            name='film_work_person_role_idx')]


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation date'), null=True)
    rating = models.FloatField(_('rating'), blank=True, null=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    file_path = models.FileField(_('file'), blank=True,
                                 null=True, upload_to='movies/')
    type = models.TextField(_('type'), choices=MovieType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        indexes = [models.Index(
            fields=['creation_date', 'rating'],
            name='film_work_creation_date_idx')]
        verbose_name = 'Фильм'
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.title
