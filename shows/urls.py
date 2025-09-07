from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shows/', views.all_shows, name='all_shows'),
    path('show/<int:show_id>/', views.show_detail, name='show_detail'),
    path('show/<int:show_id>/status/', views.update_status, name='update_status'),
    path('show/<int:show_id>/rate/', views.rate_show, name='rate_show'),
    path('episode/<int:episode_id>/watch/', views.mark_episode_watched, name='mark_episode_watched'),
]