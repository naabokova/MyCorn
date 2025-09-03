from django.shortcuts import render
from .models import Show, Episode

def index(request):
    movies_count = Show.objects.filter(type='movie').count()
    series_count = Show.objects.filter(type='series').count()
    episodes_count = Episode.objects.count()

    context = {
        'movies_count': movies_count,
        'series_count': series_count,
        'episodes_count': episodes_count,
    }
    return render(request, 'shows/home.html', context)


def all_shows(request):  # Страница со всеми фильмами и сериалами
    show_type = request.GET.get('type', '')  # Получаем параметр фильтра
    
    if show_type == 'movie':
        shows = Show.objects.filter(type='movie').order_by('title')
        title = "Фильмы"
    elif show_type == 'series':
        shows = Show.objects.filter(type='series').order_by('title')
        title = "Сериалы"
    else:
        shows = Show.objects.all().order_by('title')
        title = "Все фильмы и сериалы"
    
    context = {
        'shows': shows,
        'title': title,
        'current_filter': show_type,
        'total_count': shows.count()
    }
    
    return render(request, 'shows/all_shows.html', context)