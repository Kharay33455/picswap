from django.shortcuts import render
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

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
    if request.user.is_authenticated:
        total = request.user.artist.available_balance + request.user.artist.uncleared_balance 
        transactions = Transaction.objects.filter(user = request.user)
        images =Images.objects.filter(owner = request.user).order_by('?')
        context = {'company_name':company_name, 'images':images, 'transactions':transactions, 'total':total}
        
        return render(request, 'base/profile.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
def show(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['des']
            image = request.FILES['image']
            Images.objects.create(name = name, description = description, image=image, owner = request.user, is_featured = False )
            return HttpResponseRedirect(reverse('base:profile'))
        context = {'company_name':company_name}
        return render(request, 'base/add.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))

def copyright(request):
    if request.user.is_authenticated:
        images = Images.objects.filter(owner = request.user, is_copyright= False)
        if request.method =='POST':
            try:
                image_id = request.POST['image']
                published = request.POST['published']
                year = request.POST['year']
                co = request.POST['co']
                work_type = request.POST['work-type']
                others = request.POST['specify']
                image = Images.objects.get(id =image_id)

                Copyright.objects.create(image = image, published = published, year=year, co_authors = co, work_type = work_type, other = others)
                product_description = f'Copyright for {image.name}'
                cart, created = Cart.objects.get_or_create(owner = request.user)
                cart_item = CartItem.objects.create(product_name = f'Copyright application', product_description = product_description, product_value = 50, cart= cart)
                
                return HttpResponseRedirect(reverse('base:pay'))
            except(IntegrityError):
                msg = 'You have already submitted an application for this piece of work. Please, continue with that application.'
                
                context = {'company_name':company_name, 'images':images, 'msg':msg}
                return render(request, 'base/copyright.html', context)
        
        context = {'company_name':company_name, 'images':images}
        return render(request, 'base/copyright.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
    

def pay(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(owner = request.user)
        cart_items = CartItem.objects.filter(cart = cart)
        items = []
        for ci in cart_items:
            items.append(ci.product_value)
        total_cost = sum(items)
        total_cart_items = len(items)
        if total_cart_items<1:
            wallets = Wallet.objects.all()
            msg = 'Cart is empty'
            context = {'company_name':company_name,'msg': msg ,'wallets':wallets , 'total_cost': total_cost, 'total_cart_items':total_cart_items, 'cart_items': cart_items}
            return render(request, 'base/pay.html', context)
        if request.method =='POST':
            transaction_id = random.randint(111111111111111111, 9999999999999999999)
            wallet_id = request.POST['paymentMethod']
            wallet = Wallet.objects.get(id =wallet_id )
            wallet_network = wallet.currency
            wallet_address = wallet.address
            items=''
            for ci in cart_items:
                items = f'{items}, {ci.product_description}'
            Transaction.objects.create(transaction_id=transaction_id, user = request.user, wallet = wallet_network, wallet_address = wallet_address, total_items = total_cart_items, items = items, cost = total_cost)
            cart.delete()
            return HttpResponseRedirect(reverse('base:checkout', args=[transaction_id]))

            
        else:

            
            wallets = Wallet.objects.all()
            context = {'company_name':company_name, 'wallets':wallets , 'total_cost': total_cost, 'total_cart_items':total_cart_items, 'cart_items': cart_items}
            return render(request, 'base/pay.html', context)
        
    
    else:
        return HttpResponseRedirect(reverse('base:login'))
    
def checkout(request, t_id):
    if request.user.is_authenticated:
        transaction = Transaction.objects.get(transaction_id = t_id)

        if request.method == 'POST':
            transaction.is_paid = True
            transaction.save()
            return HttpResponseRedirect(reverse('base:profile'))
        context = {'company_name':company_name, 'transaction':transaction}
        return render(request, 'base/checkout.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
    

def acquire(request, id):
    if request.user.is_authenticated:
        piece = Images.objects.get(id = id)
        if request.method =='POST':
            chat_id = random.randint(111111111111111, 999999999999999999)
            subject = f'Bid for {piece.name}'
            buyer = Buyer.objects.get(user = request.user)
            artist = Artist.objects.get(user = piece.owner)
            chat = Chat.objects.create(chat_id = chat_id, subject=subject, buyer=buyer, artist=artist, piece=piece, read_by_artist = False, read_by_buyer = True)
            Message.objects.create(chat = chat, from_artist =False, body = 'Hi, is this still available?', image = piece.image)
            return HttpResponseRedirect(reverse('base:chat', args=[chat.chat_id]))

        
        context = {'company_name':company_name, 'piece':piece}
        return render(request, 'base/acquire.html', context)
    
    else:
        return HttpResponseRedirect(reverse('base:login'))
    
def chat(request, chat_id):
    if request.user.is_authenticated:
        chat = Chat.objects.get(chat_id = chat_id)
        buyer = Buyer.objects.get(user = chat.buyer.user)
        artist = Artist.objects.get(user = chat.artist.user)
        if request.method == 'POST':
            if request.FILES:
                image = request.FILES['image']
                body = request.POST['body']
                if request.user == artist.user:
                    Message.objects.create(chat = chat, body = body, image= image, from_artist = True)
                    buyer.has_new_message = True
                    buyer.save()
                    chat.read_by_buyer = False
                    chat.save()
                 
                else:
                    new_message = Message.objects.create(chat = chat, body=body, image=image, from_artist = False)
                    artist.has_new_message=True
                    artist.save()
                    chat.read_by_artist = False
                    chat.save()

       

            


                return HttpResponseRedirect(reverse('base:chat', args=[chat.chat_id]))
            else:
                if request.POST['body'].strip()=="":
                    return HttpResponseRedirect(reverse('base:chat', args=[chat.chat_id]))
                else:
                    body = request.POST['body']
                    if request.user == artist.user:
                        Message.objects.create(chat = chat, body=body, from_artist = True)
                        buyer.has_new_message=True
                        buyer.save()
                        chat.read_by_buyer = False
                        chat.save()
                    else:
                    
                        new_message = Message.objects.create(chat = chat, body=body, from_artist = False)
                        artist.has_new_message = True
                        artist.save()
                        chat.read_by_artist = False
                        chat.save()

           

             
                
                    return HttpResponseRedirect(reverse('base:chat', args=[chat.chat_id]))

        else:
            if request.user == chat.buyer.user:
                chat.read_by_buyer = True
                chat.save()
            else:
                chat.read_by_artist = True
                chat.save()


            messages = Message.objects.filter(chat = chat)
            context = {'chat':chat, 'buyer':buyer, 'artist':artist, 'messages':messages}
            return render(request, 'base/chat.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
    


def chats(request):
    if request.user.is_authenticated:
        request.user.buyer.has_new_message = False
        request.user.buyer.save()
        request.user.artist.has_new_message = False
        request.user.artist.save()

        sell_chats = Chat.objects.filter(artist = request.user.artist)
        buy_chats = Chat.objects.filter(buyer = request.user.buyer)
        context = {'sell_chats':sell_chats, 'buy_chats': buy_chats}
        return render(request, 'base/chats.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
    

    
"""support"""
def support(request):
    company_name = Company_name.objects.first()
    if request.user.is_authenticated:
        artist = Artist.objects.get(user = request.user)
        tickets = Ticket.objects.filter(artist = artist)
        context = {'artist':artist, 'company_name':company_name,'tickets':tickets}
        return render(request, 'base/support.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
    

"""Ticket"""

def ticket(request, number):
    company_name = Company_name.objects.first()
    if request.user.is_authenticated:
        artist = Artist.objects.get(user = request.user)
        ticket = Ticket.objects.get(ticket_id = number, artist= artist)
        if request.method == 'POST':
            if request.FILES:
                image = request.FILES['image']
                body = request.POST['body']
                new_message = Support_Message.objects.create(ticket = ticket, body=body, image=image)


                return HttpResponseRedirect(reverse('base:ticket', args=[number]))
            else:
                if request.POST['body'].strip()=="":
                    return HttpResponseRedirect(reverse('base:ticket', args=[number]))
                else:

                    body = request.POST['body']
                    new_message = Support_Message.objects.create(ticket = ticket, body=body)
                
                    return HttpResponseRedirect(reverse('base:ticket', args=[number]))
                
        
        else:
            ticket.is_read = True
            artist.has_new_message = False
            ticket.save()
            artist.save()
            messages = Support_Message.objects.filter(ticket = ticket).order_by('time_sent')

            context = {'artist':artist, 'company_name':company_name, 'ticket':ticket, 'messages':messages}
            return render(request, 'base/ticket.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))    
    
def new_issue(request):
    
    if request.user.is_authenticated:
        request.method =='POST'
        artist = Artist.objects.get(user = request.user)
        ticket_id = random.randint(111111111111111111,9999999999999999999)
        subject = request.POST['subject']
        support = Support.objects.order_by('?').first()
        new_ticket = Ticket.objects.create(ticket_id = ticket_id, subject=subject, artist=artist, support = support, is_read = True)
        body = request.POST['body']
        new_message = Support_Message.objects.create(ticket = new_ticket, body=body)
        reply_message = Support_Message.objects.create(ticket=new_ticket, body ='We will reply you shortly. Note; This message is auto-generated.', from_support = True)
        return HttpResponseRedirect(reverse('base:ticket', args= [ticket_id]))        
    else:
        return HttpResponseRedirect(reverse('base:login'))
    

def pfp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            photo = request.FILES['photo']
            request.user.buyer.pfp = photo
            request.user.buyer.save()
            request.user.artist.pfp = request.user.buyer.pfp
            request.user.artist.save()
            return HttpResponseRedirect(reverse('base:profile'))
        else:
            request.user.buyer.pfp.delete()
            request.user.artist.pfp.delete()
            return HttpResponseRedirect(reverse('base:profile'))
    else:
        return HttpResponseRedirect(reverse('base:login'))
    

def delete_cart_item(request, id):
    if request.user.is_authenticated:
        CartItem.objects.get(id = id).delete()
        return HttpResponseRedirect(reverse('base:pay'))

    else:
        return HttpResponseRedirect(reverse('base:login'))

def delete_art_piece(request, id):
    if request.user.is_authenticated:
        Images.objects.get(id = id).delete()
        return HttpResponseRedirect(reverse('base:profile'))

    else:
        return HttpResponseRedirect(reverse('base:login')) 
    
def offer(request, id):
    if request.user.is_authenticated:
        request.method = 'POST'
        offer = request.POST['offer']
        chat = Chat.objects.get(id = id)
        chat.offer = offer
        chat.save()
        return HttpResponseRedirect(reverse('base:chat', args=[chat.chat_id]))
    


    else:
        return HttpResponseRedirect(reverse('base:login'))
    
def swap(request, chat_id):
    if request.user.is_authenticated:
        chat = Chat.objects.get(chat_id = chat_id)
        chat.artist.uncleared_balance+=chat.offer
        chat.artist.save()
        chat.piece.owner = chat.buyer.user
        chat.piece.save()
        Swap.objects.create(swap_id = chat_id, buyer = chat.buyer.name, artist = chat.artist.name, piece = chat.piece.name, piece_description = chat.piece.description, price = chat.offer)
        return HttpResponseRedirect(reverse('base:profile'))
    
    
    else:
        return HttpResponseRedirect(reverse('base:login'))