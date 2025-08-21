from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Страница приложения shows")

def categories(request):
    return HttpResponse("<h1>Категории</h1>")