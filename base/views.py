from django.shortcuts import render

# Create your views here.

def base(request):
    context = {}
    return render (request, 'base/index.html', context)

def featured(request):
    context = {}
    return render (request, 'base/featured.html', context)

def about(request):
    context = {}
    return render(request, 'base/about.html', context)
