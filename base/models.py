from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SuperUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_edited_des = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

class Company_name(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.name}'
    

class Artist(models.Model):
    name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_new_message = models.BooleanField(default=False)
    pfp = models.ImageField(blank=True, null=True, upload_to='images')
    available_balance = models.IntegerField(default=0)
    uncleared_balance = models.IntegerField(default=0)
    swaps_completed = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.name}'

class Images(models.Model):
    image_id = models.CharField(max_length=20)
    name = models.CharField(max_length = 30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    is_featured = models.BooleanField()
    is_copyright= models.BooleanField(default=False)
    date_uploaded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
    
class Buyer(models.Model):
    name = models.CharField(max_length = 30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_new_message = models.BooleanField(default=False)
    pfp = models.ImageField(blank=True, null=True, upload_to='images/pfp')

    def __str__(self):
        return f'{self.name}'
    

class Copyright(models.Model):
    image = models.OneToOneField(Images, on_delete=models.CASCADE)
    published = models.CharField(max_length=4)
    year = models.CharField(max_length=4)
    co_authors = models.CharField(max_length=30, blank=True, null=True)
    work_type = models.CharField(max_length=10)
    other = models.CharField(max_length=10, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f'Copyright proceedings for {self.image.name}'
    

class Wallet(models.Model):
    currency = models.CharField(max_length=10)
    network = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.currency} {self.network} wallet'
    
class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.owner.username}\'s cart'
    
class CartItem(models.Model):
    product_name = models.CharField(max_length=20)
    product_description = models.CharField(max_length=50)
    product_value = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_name}'

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.CharField(max_length=10)
    wallet_address = models.CharField(max_length=50)
    total_items = models.IntegerField()
    items = models.CharField(max_length=50)
    cost = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} transaction on {self.date}'


class Chat(models.Model):
    chat_id = models.CharField(max_length=20)
    subject = models.CharField(max_length=30)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    piece = models.ForeignKey(Images, on_delete=models.CASCADE)
    read_by_artist = models.BooleanField()
    read_by_buyer = models.BooleanField()
    date_of_creation = models.DateTimeField(auto_now_add=True)
    offer = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    err = models.CharField(max_length=50, blank = True, null=True)
    artist_err = models.CharField(max_length=50, blank=True, null=True)

    

    def __str__(self):
        return f'Chat between {self.buyer} and {self.artist}'
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    from_artist =models.BooleanField()
    body = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f'Message from {self.chat}'




"""Support functionality"""
    
"""Implementing the support function"""
class Support(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=20)
    pfp = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.name}'
    
class Ticket(models.Model):
    ticket_id = models.CharField(max_length=20)
    subject = models.CharField(max_length=30)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    support = models.ForeignKey(Support, on_delete=models.CASCADE)
    is_read= models.BooleanField(default=False)
    date_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject} ticket by {self.artist.user.username} on {self.date_of_creation}//Is read? {self.is_read}'
    

class Support_Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete = models.CASCADE)
    body = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    from_support = models.BooleanField(default=False)
    time_sent = models.DateTimeField(auto_now_add=True)
    is_replied = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.from_support == True:
            self.ticket.is_read = False
            self.ticket.save()
            self.ticket.artist.has_new_message = True
            self.ticket.artist.save()
        super(Support_Message, self).save(*args, **kwargs)

    def __str__(self):
        if self.from_support == True:
            return f'Reply to {self.ticket.artist.user.first_name} {self.ticket.artist.user.last_name} / is_replied? {self.is_replied}'
        else:
            return f'Message from {self.ticket.artist.user.first_name} {self.ticket.artist.user.last_name} / is_replied? {self.is_replied}'




"""Record successfull swaps"""
class Swap(models.Model):
    swap_id = models.CharField(max_length=20)
    buyer = models.CharField(max_length=30)
    artist = models.CharField(max_length=30)
    piece = models.CharField(max_length=30)
    piece_description = models.TextField()
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.artist} sold {self.piece} to {self.buyer} at {self.price} on {self.date}'
    
"""Steps"""
class Step(models.Model):
    picture = models.ImageField(upload_to='images/steps')
    header = models.CharField(max_length=50)
    step = models.TextField()
    note = models.TextField()

    def __str__(self):
        return f'{self.header}'
