from django.shortcuts import render
from .models import Show
from django.http import HttpResponse, HttpResponseNotFound


# def home(request):
#     show = Show.object.all().order_by('-id')[:10]
#     return render(request, 'show/home.html', {'shows': show})


def index(request):
    return HttpResponse("Страница приложения shows")

def categories(request, cat_id):
    return HttpResponse(f"<h1>Категории</h1><p>id: {cat_id}</p>") #для каждого show будет свой номер 


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Категории</h1><p>slug: {cat_slug}</p>") # поменять на str

def archive(request, year):
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")  # красивенько отобразит ошибку