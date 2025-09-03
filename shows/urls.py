from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shows/', views.all_shows, name='all_shows')
]