from django.shortcuts import render
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
company_name = Company_name.objects.first()


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

def login_request(request):
    company_name = Company_name.objects.first()
    if request.method == 'POST':
        try:
            if "@" in request.POST['username']:
                try:
                    possible_user = User.objects.get(email = request.POST['username'])
                    usernames = possible_user.username
                except(KeyError, User.DoesNotExist):
                    usernames = request.POST['username']
            else:

                username = request.POST['username']
                usernames = username.replace(" ","")
            password = request.POST['password1']
            passwords = password.replace(' ','')
            user = authenticate(request, username = usernames, password = passwords)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('base:home'))
            else:
                context = {'err':'Invalid username or password', 'company_name':company_name}
                return render(request, 'base/login.html', context)
        except (KeyError, User.DoesNotExist):
            context = {'err':'User Does Not Exist', 'company_name':company_name}
            return render(request, 'base/login.html', context)
    else:

        return render(request, 'base/login.html')
    

def register_request(request):
    company_name = Company_name.objects.first()
    #checking if method is post
    if request.method == 'POST':
        try:
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            first_name = first_name.replace(' ','')
            last_name = last_name.replace(' ','')
            username = username.replace(' ','')
            email = email.replace(' ','')
            password1 = password1.replace(' ','')
            password2 = password2.replace(' ','')
            if password1 == password2:

                new_user = User.objects.create_user(username=username, first_name = first_name, 
                                                    last_name =last_name, password=password1, email= email)
                new_user.save()
                artist = Artist.objects.create(user = new_user, name=username)
                buyer = Buyer.objects.create(user = new_user, name = username)

                login(request, new_user)
                return HttpResponseRedirect(reverse('base:home'))
            else:
                context = {'err':'Your passwords didn\'t match', 'company_name':company_name}
                return render (request, 'base/register.html', context)
        except (IntegrityError):
            context = {'err': 'A user with this username already exists.', 'company_name':company_name}
            return render(request, 'base/register.html', context)
    context = {'company_name':company_name}
    return render(request, 'base/register.html', context)



def logout_request(request):
    company_name = Company_name.objects.first()
    logout(request)
    return HttpResponseRedirect(reverse('base:home'))

def profile(request):
    context = {'company_name':company_name}
    return render(request, 'base/profile.html', context)

