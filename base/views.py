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
    company_name = Company_name.objects.first()
    steps = Step.objects.all()

    context = {'company_name':company_name, 'steps':steps}

    return render (request, 'base/index.html', context)

def featured(request):
    company_name = Company_name.objects.first()

    featured = Images.objects.filter(is_featured = True).order_by('?')
    featured = featured[:30]
    context = {'featured':featured, 'company_name':company_name}
    return render (request, 'base/featured.html', context)

def about(request):
    company_name = Company_name.objects.first()

    context = {'company_name':company_name}
    return render(request, 'base/about.html', context)

def pricing(request):
    company_name = Company_name.objects.first()

    context = {'company_name':company_name}
    return render(request, 'base/pricing.html', context)

def details(request, id):
    company_name = Company_name.objects.first()

    try:
        piece = Images.objects.get(image_id = id)
        context ={'piece':piece, 'company_name':company_name}
        return render(request, 'base/featured_details.html', context)
    except(KeyError, Images.DoesNotExist):
        featured = Images.objects.filter(is_featured = True).order_by('?')
        context = {'company_name':company_name, 'featured':featured, 'err':'We couldn\'t find this art piece on any of our servers. Please double-check that you\'ve entered the correct ID.'}
        return render (request, 'base/featured.html', context)


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
    company_name = Company_name.objects.first()

    if request.user.is_authenticated:
        total = request.user.artist.available_balance + request.user.artist.uncleared_balance 
        transactions = Transaction.objects.filter(user = request.user)
        images =Images.objects.filter(owner = request.user).order_by('?')
        swaps = Swap.objects.filter(buyer = request.user.buyer.name)
        swaps2 = Swap.objects.filter(artist = request.user.artist.name)
        context = {'company_name':company_name, 'images':images, 'transactions':transactions, 'total':total, 'swaps':swaps, 'swaps2':swaps2}
        
        return render(request, 'base/profile.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
def show(request):
    company_name = Company_name.objects.first()

    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['des']
            if description =='':
                description = request.POST['name']
            else:
                description = request.POST['des']
            image = request.FILES['image']
            img_id = random.randint(1111111111,9999999999999999)
            Images.objects.create(name = name, description = description, image=image, owner = request.user, is_featured = False, image_id =img_id )
            return HttpResponseRedirect(reverse('base:profile'))
        context = {'company_name':company_name}
        return render(request, 'base/add.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))

def copyright(request):
    company_name = Company_name.objects.first()

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
                msg = f'You have already submitted an application for {image.name}. Please, continue with that application.'
                
                context = {'company_name':company_name, 'images':images, 'msg':msg}
                return render(request, 'base/copyright.html', context)
        
        context = {'company_name':company_name, 'images':images}
        return render(request, 'base/copyright.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
    

def pay(request):
    company_name = Company_name.objects.first()

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
    company_name = Company_name.objects.first()

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
    company_name = Company_name.objects.first()

    if request.user.is_authenticated:
        piece = Images.objects.get(id = id)
        if request.method =='POST':
            chat_id = random.randint(111111111111111, 999999999999999999)
            subject = f'Bid for {piece.name}'
            buyer = Buyer.objects.get(user = request.user)
            artist = Artist.objects.get(user = piece.owner)
            chat = Chat.objects.create(chat_id = chat_id, subject=subject, buyer=buyer, artist=artist, piece=piece, read_by_artist = False, read_by_buyer = True)
            Message.objects.create(chat = chat, from_artist =False, body = 'Hi, is this still available?', image = piece.image)
            chat.artist.has_new_message = True
            chat.artist.save()
            return HttpResponseRedirect(reverse('base:chat', args=[chat.chat_id]))

        
        context = {'company_name':company_name, 'piece':piece}
        return render(request, 'base/acquire.html', context)
    
    else:
        return HttpResponseRedirect(reverse('base:login'))
    
def chat(request, chat_id):
    company_name = Company_name.objects.first()

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
            context = {'chat':chat, 'buyer':buyer, 'artist':artist, 'messages':messages, 'company_name':company_name}
            return render(request, 'base/chat.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
    


def chats(request):
    company_name = Company_name.objects.first()

    if request.user.is_authenticated:
        request.user.buyer.has_new_message = False
        request.user.buyer.save()
        request.user.artist.has_new_message = False
        request.user.artist.save()

        sell_chats = Chat.objects.filter(artist = request.user.artist)
        buy_chats = Chat.objects.filter(buyer = request.user.buyer)
        context = {'sell_chats':sell_chats, 'buy_chats': buy_chats, 'company_name':company_name}
        return render(request, 'base/chats.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
    

    
"""support"""
def support(request):
    company_name = Company_name.objects.first()

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
    company_name = Company_name.objects.first()

    
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
    company_name = Company_name.objects.first()

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
    company_name = Company_name.objects.first()

    if request.user.is_authenticated:
        CartItem.objects.get(id = id).delete()
        return HttpResponseRedirect(reverse('base:pay'))

    else:
        return HttpResponseRedirect(reverse('base:login'))

def delete_art_piece(request, id):
    company_name = Company_name.objects.first()

    if request.user.is_authenticated:
        Images.objects.get(id = id).delete()
        return HttpResponseRedirect(reverse('base:profile'))

    else:
        return HttpResponseRedirect(reverse('base:login')) 
    
def offer(request, id):
    company_name = Company_name.objects.first()

    if request.user.is_authenticated:
        chat = Chat.objects.get(id = id)

        if request.method == 'POST':
        
            offer = request.POST['offer']
            
            if int(offer) < chat.buyer.user.artist.available_balance :
                chat.buyer.user.artist.available_balance -= int(offer)
                chat.buyer.user.artist.save()
                chat.artist.has_new_message = True
                chat.artist.save()

                chat.offer = offer
                chat.save()
                return HttpResponseRedirect(reverse('base:chat', args=[chat.chat_id]))
            else:
                chat.err = 'You do not have enough balance to complete this transaction'
                chat.save()
                return HttpResponseRedirect(reverse('base:chat', args=[chat.chat_id]))
        else:
            
            chat.buyer.user.artist.available_balance += int(chat.offer)
            chat.buyer.user.artist.save()
            chat.buyer.has_new_message = True
            chat.buyer.save()
            
            chat.err = f'{chat.artist} rejected your offer of ${chat.offer}'
            chat.artist_err = f'You rejected {chat.buyer}\'s offer of ${chat.offer}'
            chat.offer = None
            chat.save()
            return HttpResponseRedirect(reverse('base:chat', args=[chat.chat_id]))

            


    else:
        return HttpResponseRedirect(reverse('base:login'))
    
def swap(request, chat_id):
    company_name = Company_name.objects.first()

    if request.user.is_authenticated:
        chat = Chat.objects.get(chat_id = chat_id)
        chat.artist.uncleared_balance+=chat.offer
        chat.artist.swaps_completed +=1
        chat.artist.save()
        chat.buyer.user.artist.swaps_completed+=1
        chat.buyer.user.artist.save()
        chat.piece.owner = chat.buyer.user
        chat.piece.save()
        Swap.objects.create(swap_id = chat_id, buyer = chat.buyer.name, artist = chat.artist.name, piece = chat.piece.name, piece_description = chat.piece.description, price = chat.offer)
        chat.completed = True
        chat.save()
        return HttpResponseRedirect(reverse('base:chat', args=[chat.chat_id]))
    
    
    else:
        return HttpResponseRedirect(reverse('base:login'))
    

def upgrade(request, package):
    company_name = Company_name.objects.first()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(owner = request.user)
        if package == 'established':
            CartItem.objects.create(product_name = 'Established Artist upgrade', product_description = 'Buy and get access to more features', product_value = 15, cart = cart)
            return HttpResponseRedirect(reverse('base:pay'))
        else:
            CartItem.objects.create(product_name = 'Renowned Artist upgrade', product_description = 'Unlock unlimited possibilities to potential clients', product_value = 29, cart=cart)
            return HttpResponseRedirect(reverse('base:pay'))

    else:
        return HttpResponseRedirect(reverse('base:login'))
    

def search(request):
    company_name = Company_name.objects.first()

    if request.user.is_authenticated:
        if request.method =='POST':
                
                image_id = request.POST['image_id'].strip()
                image_id = "".join(image_id.split())
                return HttpResponseRedirect(reverse('base:details', args=[image_id]))
    else:
        return HttpResponseRedirect(reverse('base:login'))
    
    

import os
from datetime import datetime
def create(request):
#    files = r"C:\Users\ASUS\Downloads\From_kharay-20240714T141001Z-001\pfp"
 #   files = os.listdir(files)



            
   

    #counter = 0
    #for owner in owners:
     #   images = Images.objects.filter(owner = owner)
      #  for photo in images:
       #     counter+=1
    #print(counter)
      #  for photo in images:
       #     photo.image = f'images/{photo.image}'
        #    photo.save()
    return HttpResponseRedirect(reverse('base:home'))


#def create(request):

  #  files = r"C:\Users\ASUS\Downloads\From_kharay-20240714T141001Z-001\From_kharay"
    
 #   art_words = ['Whisper', 'Echo', 'Serenity', 'Harmony', 'Tranquil', 'Ethereal', 'Celestial', 'Radiant', 'Mystic', 'Enchanted', 'Cosmic', 'Luminous', 'Dreamscape', 'Melody', 'Symphony', 'Silent', 'Twilight', 'Ocean', 'Forest', 'Reflection', 'Journey', 'Mirage', 'Horizon', 'Blossom', 'Aurora', 'Vibrant', 'Enigma', 'Sacred', 'Starlit', 'Infinite', 'Sublime', 'Sapphire', 'Crimson', 'Emerald', 'Golden', 'Eden', 'Meadow', 'Garden', 'Spring', 'Autumn', 'Winter', 'Dawn', 'Sunset', 'Rainbow', 'Miracle', 'Whirlwind', 'Cascade', 'Cathedral', 'Shadow', 'Essence', 'Solitude', 'Passion', 'Joy', 'Hope', 'Destiny', 'Timeless', 'Whispering', 'Enchanted', 'Epic', 'Majestic', 'Mystery', 'Tranquility', 'Fantasy', 'Serendipity', 'Synchronicity', 'Ethereal', 'Breathtaking', 'Inspiration', 'Nebula', 'Phenomenon', 'Harmony', 'Intrigue', 'Surreal', 'Infinity', 'Whisper', 'Luminosity', 'Reflection', 'Eclipse', 'Delight', 'Spellbound', 'Spectacle', 'Marvel', 'Enchantment', 'Stardust', 'Illusion', 'Zenith', 'Wonder', 'Rapture', 'Pulse', 'Embrace', 'Radiance', 'Dream', 'Mystical', 'Aura', 'Dance', 'Bliss', 'Landscape', 'Abstract', 'Canvas', 'Vivid', 'Elegance', 'Mosaic', 'Color', 'Form', 'Shape', 'Vision', 'Imagination', 'Silhouette', 'Sketch', 'Palette', 'Texture', 'Shade']


  #  first_names = [
   # "Liam",
   # "Olivia",
   ## "Noah",
 #   "Emma",
  #  "Jackson",
   # "Ava",
 #   "Aiden",
  #  "Sophia",
   # "Lucas",
 #   "Isabella",
  #  "Caden",
   # "Mia",
  #  "Grayson",
   # "Amelia",
 #   "Mason",
  #  "Harper",
   # "Elijah",
 #   "Evelyn",
  #  "Logan",
   # "Abigail",
 #   "Carter",
  #  "Emily",
   # "James",
 ##  "Alexander",
   # "Charlotte",
  #  "Benjamin",
   # "Ella",
   # "William",
    #"Scarlett"]

   # last_names_asian = [
    #"Li",
    #"Wang",
    #"Zhang",
    #"Liu",
    #"Chen",
    #"Yang",
    #"Huang",
    #"Zhao",
    #"Zhu",
    #"Lin",
    #"Xu",
    #"Sun",
    #"Ma",
    #"Gao",
    #"Hu",
    #"Liao",
    #"Wu",
    #"He",
    #"Guo",
    #"Jiang",
    #"Deng",
    #"Xie",
    #"Fu",
    #"Han",
    #"Tang",
    #"Kang",
    #"Yuan",
    #"Yao",
    #Qin",
    #"Feng"]
    #usernames = [
   # "BlueSky123",
   # "SilverStar82",
   # "DreamCatcher",
   # "NeonNinja",
   # "EchoFlame",
   # "LunarLion",
   # "MysticDragon",
   # "PixelPilot",
   # "CyberScribe",
   # "JadeJester",
   # "PhoenixFire",
   # "StormRider",
   # "SolarSailor",
   # "CosmicComet",
   # "StarDancer",
   # "RavenWing",
   # "AlphaOmega",
   # "NovaKnight",
   # "TigerEye",
   # "SerenitySeeker",
    #"WildWhisper",
    #"EnigmaExplorer",
    #"EternalEcho",
    #"GalacticGazer",
  ## "QuasarQuest",
 #   "ZephyrZephyr",
  #  "SilentShadow",
   # "AstralAdventurer",
   #"LuminousLynx"]


  #  for username in usernames:
   #     f = random.randint(0,29)
    #    l = random.randint(0,29)
     #   new_user = User.objects.create_user(first_name = first_names[f], last_name = last_names_asian[l], username = username, password='Asdfghjkl1_', email='kray@gmail.com')
      #  new_user.save()
       # Artist.objects.create(name = username, user = new_user)
       # Buyer.objects.create(name = username, user = new_user)
    
  #  print('All users created successfully')

#    for file in os.listdir(files):
 #       image_id = random.randint(1111111111111111,9999999999999999999)
  #      name_rand = random.randint(0, 3)
   #     alias1 = random.randint(0,19)
    #    alias2 = random.randint(0,19)
     #   alias3 = random.randint(0,19)
      #  alias4 = random.randint(0,19)
      # if name_rand ==0:
       #     name = f'{art_words[alias1]} and {art_words[alias2]}'
       # elif name_rand ==1:
        #    name = f'The {art_words[alias1]} of {art_words[alias2]} and {art_words[alias3]}'
#        elif name_rand ==2:
 #           name = f'{art_words[alias1]} the {art_words[alias2]} of {art_words[alias3]} and {art_words[alias4]}'
  ##         name = f'The {art_words[alias4]} {art_words[1]}'
    #    owner = User.objects.filter(email = 'kray@gmail.com').order_by('?').first()


     #   Images.objects.create(image_id = image_id, name = name, owner=owner, description = name, image = file, is_featured = True, is_copyright = True)

   # return HttpResponseRedirect(reverse('base:home'))




def edit(request, id):
    piece = Images.objects.get(id = id)
    if request.user.is_staff:
        if request.method == 'POST':
            new_description = request.POST['des']
            piece.description = new_description
            piece.save()
            edited = SuperUser.objects.get(user = request.user)
            edited.has_edited_des +=1
            edited.save()
            return HttpResponseRedirect(reverse('base:details', args=[piece.image_id]))

        else:
            
            context = {'piece':piece}
            return render(request, 'base/edit.html', context)
    else:
        return HttpResponseRedirect(reverse('base:home'))