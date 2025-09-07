from django.shortcuts import render, get_object_or_404, redirect
from .models import Show, Episode, UserShowStatus, WatchedEpisode, UserRating
from .models import UserShowStatus
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


def show_detail(request, show_id):
    # Находим фильм/сериал по ID или показываем ошибку 404
    show = get_object_or_404(Show, id=show_id) 
    # Проверяем, есть ли у пользователя статус для этого шоу
    user_status = None
    episodes = []
    watched_episodes = []
    if request.user.is_authenticated: 
        user_status = UserShowStatus.objects.filter(user=request.user, show=show).first()
        user_rating_obj = UserRating.objects.filter(user=request.user, show=show).first()
        user_rating = user_rating_obj.rating if user_rating_obj else None
        
        if show.type == 'series':
            episodes = Episode.objects.filter(show=show).order_by('season_number', 'episode_number')
            watched_episodes = WatchedEpisode.objects.filter(
                user=request.user, 
                episode__show=show
            ).values_list('episode_id', flat=True)
    else:
        user_rating = None 
    
    context = {
        'show': show,
        'user_status': user_status,
        'episodes': episodes,
        'watched_episodes': list(watched_episodes),
        'user_rating': user_rating,  
    }
    
    return render(request, 'shows/show_detail.html', context)

@login_required
def rate_show(request, show_id):
    """Оценка фильма/сериала пользователем"""
    show = get_object_or_404(Show, id=show_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        
        if rating and rating.isdigit():
            rating_value = int(rating)
            
            if 1 <= rating_value <= 10:
                # Создаем или обновляем оценку
                UserRating.objects.update_or_create(
                    user=request.user,
                    show=show,
                    defaults={'rating': rating_value}
                )
                messages.success(request, 'Ваша оценка сохранена!')
            else:
                messages.error(request, 'Оценка должна быть от 1 до 10')
        else:
            messages.error(request, 'Пожалуйста, выберите оценку')
    
    return redirect('show_detail', show_id=show_id)


@login_required
def update_status(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['watching', 'stopped', 'planned', 'watched']:
            # Просто обновляем статус без сложной формы
            UserShowStatus.objects.update_or_create(
                user=request.user,
                show=show,
                defaults={'status': status}
            )
    
    return redirect('show_detail', show_id=show_id)


@login_required
def mark_episode_watched(request, episode_id):
    episode = get_object_or_404(Episode, id=episode_id)
    # Создаем запись о просмотре
    WatchedEpisode.objects.get_or_create(
        user=request.user,
        episode=episode
    )
    
    return redirect('show_detail', show_id=episode.show.id)