from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  #главная страница /
    path('cats/', views.categories),  #/cats/
]