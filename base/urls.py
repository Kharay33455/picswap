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
    path('profile',views.profile, name='profile'),
    path('show-and-tell', views.show, name="show"),
    path('learn-more-about-copyright', views.copyright, name='copyright'),
    path('pay', views.pay, name="pay"),
    path('pay/checkout<slug:t_id>', views.checkout, name ='checkout'),
    path('featured/<int:id>28698/acquire', views.acquire, name='acquire'),
    path('chat/<int:chat_id>', views.chat, name='chat'),

]