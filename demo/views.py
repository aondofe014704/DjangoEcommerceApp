from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, Jack Songu")


def homepage(request):
    return render(request, 'home.html', {"name": "James Brown"})
