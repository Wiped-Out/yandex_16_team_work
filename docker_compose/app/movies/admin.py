from django.contrib import admin

from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 0


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', 'created', 'modified')

    # Фильтрация в списке
    list_filter = ('created', 'modified')

    # Поиск по полям
    search_fields = ('name', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('full_name', 'created', 'modified')

    # Фильтрация в списке
    list_filter = ('created', 'modified')

    # Поиск по полям
    search_fields = ('full_name', 'description', 'id')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,
               PersonFilmworkInline)
    list_prefetch_related = ('genres', 'persons')

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date',
                    'rating', 'get_genres',
                    'created', 'modified')

    # Фильтрация в списке
    list_filter = ('type', 'creation_date', 'created', 'modified')

    # Поиск по полям
    search_fields = ('title', 'description', 'id')

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request)
                   .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join(genre.name for genre in obj.genres.all())

    get_genres.short_description = 'Жанры фильма'
