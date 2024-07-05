from django.shortcuts import render
from .models import *

# Create your views here.

def base(request):
    context = {}
    return render (request, 'base/index.html', context)

def featured(request):
    featured = Images.objects.filter(is_featured = True).order_by('?')
    context = {'featured':featured}
    return render (request, 'base/featured.html', context)

def about(request):
    context = {}
    return render(request, 'base/about.html', context)

def pricing(request):
    context = {}
    return render(request, 'base/pricing.html', context)

def details(request, id):
    piece = Images.objects.get(id = id)
    context ={'piece':piece}
    return render(request, 'base/featured_details.html', context)
