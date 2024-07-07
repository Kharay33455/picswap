from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company_name(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.name}'
    

class Artist(models.Model):
    name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_new_message = models.BooleanField(default=False)
    
    

    def __str__(self):
        return f'{self.name}'

class Images(models.Model):
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

    

    def __str__(self):
        return f'Chat between {self.buyer} and {self.artist}'
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    from_artist =models.BooleanField()
    body = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f'Message from {self.chat}'