from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index),  #главная страница /
    path('cats/<int:cat_id>/', views.categories),  #/cats/
    path('cats/<slug:cat_slug>/', views.categories_by_slug),  #сделаю str для категорий
    path("archive/<year4:year>/", views.archive)  #вызов строго по 4 цифрам
]