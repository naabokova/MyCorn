from django.db import models
from django.contrib.auth.models import User 


class Genre(models.Model):  # Форма для жанра
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Show(models.Model):  # Форма для сериала
    title = models.CharField(max_length=250)
    description = models.TextField() 
    poster = models.ImageField(upload_to='posters/', blank=True)
    genres = models.ManyToManyField(Genre)  # у сериала может быть несколько жанров
    release_year = models.ImageField
    
    def __str__(self):
        return self.title
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)