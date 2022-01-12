from django.shortcuts import render, HttpResponse

# Create your views here.
def databaseHome(request):
    return HttpResponse("Hola, esta es una app para mantener los modelos :)")