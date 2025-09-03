from django.contrib import admin
from .models import Genre, Show, Episode, UserShowStatus, WatchedEpisode


admin.site.register(Genre)
admin.site.register(Show)
admin.site.register(Episode)
admin.site.register(UserShowStatus)
admin.site.register(WatchedEpisode)

