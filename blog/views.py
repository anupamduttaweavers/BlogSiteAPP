from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
def base(request):
    return render(request, 'base.html')