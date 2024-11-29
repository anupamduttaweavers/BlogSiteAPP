from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, 'BlogApp/home.html/', context={})
