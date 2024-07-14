from django.urls import path
from . import views

app_name = 'base'

urlpatterns =[
    path('', views.base, name='home'),
    path('featured', views.featured, name='featured'),
    path('featured/search', views.search, name='search'),

    path('about', views.about, name='about'),
    path('pricing', views.pricing, name='pricing'),
    path('pricing/upgrade<slug:package>', views.upgrade, name='upgrade'),

    path('featured/<int:id>28698', views.details, name='details'),
    path('featured/<int:id>28698/delete', views.delete_art_piece, name='delete-piece'),
    path('login', views.login_request, name='login'),
    path('register', views.register_request, name='register'),
    path('logout', views.logout_request, name='logout'),
    path('profile',views.profile, name='profile'),
    path('profile/change-pfp', views.pfp, name='pfp'),
    path('show-and-tell', views.show, name="show"),
    path('learn-more-about-copyright', views.copyright, name='copyright'),
    path('pay', views.pay, name="pay"),
    path('pay/delete<int:id>', views.delete_cart_item, name='delete'),
    path('pay/checkout<slug:t_id>', views.checkout, name ='checkout'),
    path('featured/<int:id>28698/acquire', views.acquire, name='acquire'),
    path('chats/chat/<int:chat_id>', views.chat, name='chat'),
    path('chats/chat/<int:id>28698/make-offer', views.offer, name='offer'),
    path('swap<int:chat_id>', views.swap, name = 'swap'),
    path('chats', views.chats, name='chats'),
    path('support/', views.support, name='support'),
    path('support/ticket<slug:number>', views.ticket, name='ticket'),
    path('support/new-issue', views.new_issue, name='new_issue'),
    #path('create', views.create, name = 'create'),

]