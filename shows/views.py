from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Страница приложения shows")

def categories(request, cat_id):
    return HttpResponse(f"<h1>Категории</h1><p>id: {cat_id}</p>") #для каждого show будет свой номер 


def categories_by_slug(request, cat_slug):
    return HttpResponse(f"<h1>Категории</h1><p>slug: {cat_slug}</p>") # поменять на str

def archive(request, year):
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")