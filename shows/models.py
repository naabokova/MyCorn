from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):  # Модель для жанров фильмов/сериалов. может принадлежать многим фильмам (Many-to-Many)
    name = models.CharField(
        max_length=255,   
        unique=True,   # unique=True - названия жанров должны быть уникальными
        verbose_name="Название жанра"  # verbose_name - человекочитаемое название для админки
    )
    

    def __str__(self):  # Строковое представление объекта (для админки)
        return self.name

    class Meta:
        verbose_name = "Жанр"          # Название в единственном числе
        verbose_name_plural = "Жанры"  # Название во множественном числе


class Show(models.Model):  # Основная модель для фильмов и сериалов.
    TYPE_CHOICES = [
        ('movie', 'Фильм'),
        ('series', 'Сериал'),
    ]  # Выбор типа: фильм или сериал
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип")  # Изображение (загрузка файлов)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, verbose_name="Постер")
    release_date = models.DateField(verbose_name="Дата выхода", null=True, blank=True)   # Даты и время
    duration = models.PositiveIntegerField(help_text="Продолжительность в минутах", verbose_name="Длительность", null=True, blank=True) # Числовые поля
    imdb_rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], blank=True, null=True, verbose_name="Рейтинг IMDB")  # Рейтинги с валидацией
    kinopoisk_rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], blank=True, null=True, verbose_name="Рейтинг Кинопоиск")
    genres = models.ManyToManyField(Genre, related_name='shows', verbose_name="Жанры")  # Связь Many-to-Many с жанрами
    total_seasons = models.PositiveIntegerField(default=1, verbose_name="Всего сезонов")  # Поля для сериалов
    total_episodes = models.PositiveIntegerField(default=1, verbose_name="Всего серий")

    def __str__(self):
        year = self.release_date.year if self.release_date else 'н/д'
        return f"{self.title} ({year})"

    class Meta:
        verbose_name = "Фильм/Сериал"
        verbose_name_plural = "Фильмы/Сериалы"


class Episode(models.Model):  #Модель для эпизодов сериалов. сериал имеет много эпизодов (One-to-Many)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='episodes', verbose_name="Сериал")
    season_number = models.PositiveIntegerField(verbose_name="Номер сезона")  # Номера сезона и серии
    episode_number = models.PositiveIntegerField(verbose_name="Номер серии")
    title = models.CharField(max_length=255, verbose_name="Название серии")
    air_date = models.DateField(verbose_name="Дата выхода серии", null=True, blank=True)
    

    class Meta:   # Уникальная комбинация: сериал + сезон + серия
        unique_together = ('show', 'season_number', 'episode_number')
        ordering = ['season_number', 'episode_number']  # Сортировка по умолчанию
        verbose_name = "Эпизод"
        verbose_name_plural = "Эпизоды"

    def __str__(self):
        return f"{self.show.title} - S{self.season_number}E{self.episode_number} {self.title}"
    

class UserShowStatus(models.Model):  #Статус просмотра для пользователя.Связь между User и Show с дополнительной информацией.
    STATUS_CHOICES = [
        ('watching', 'Смотрю'),
        ('stopped', 'Перестал смотреть'),
        ('planned', 'Буду смотреть'),
        ('watched', 'Просмотрено'),
    ]
    
    # Связи с пользователем и шоу
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='show_statuses')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='user_statuses')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='planned')  # Статус просмотра
    
    # Прогресс просмотра (для сериалов)
    current_season = models.PositiveIntegerField(default=1)
    current_episode = models.PositiveIntegerField(default=0)

    class Meta:   # Один пользователь может иметь только один статус для каждого шоу
        unique_together = ('user', 'show')
        verbose_name = "Статус просмотра"
        verbose_name_plural = "Статусы просмотра"

    def __str__(self):
        return f"{self.user.username} - {self.show.title} ({self.status})"
    

class WatchedEpisode(models.Model):  #Отметки о просмотренных сериях с оценками и комментариями.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watched_episodes')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='watched_by')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True, verbose_name="Оценка пользователя")  # Оценка с валидацией
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    watched_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата просмотра")

    class Meta:
        unique_together = ('user', 'episode')  # Нельзя отметить одну серию дважды
        verbose_name = "Просмотренная серия"
        verbose_name_plural = "Просмотренные серии"

    def __str__(self):
        return f"{self.user.username} watched {self.episode}"