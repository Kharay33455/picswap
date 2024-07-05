from django.urls import path
from . import views

app_name = 'base'

urlpatterns =[
    path('', views.base, name='home'),
    path('featured', views.featured, name='featured'),
    path('about', views.about, name='about'),
]