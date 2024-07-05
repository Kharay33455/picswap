from django.urls import path
from . import views

app_name = 'base'

urlpatterns =[
    path('', views.base, name='home'),
    path('featured', views.featured, name='featured'),
    path('about', views.about, name='about'),
    path('pricing', views.pricing, name='pricing'),
    path('featured/<int:id>28698', views.details, name='details'),
    path('login', views.login_request, name='login'),
    path('register', views.register_request, name='register'),
    path('logout', views.logout_request, name='logout'),
]