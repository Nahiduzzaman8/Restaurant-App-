from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name


class Items(models.Model):
    item_name = models.CharField(max_length=20)
    description = models.TextField(blank=False)
    price = models.IntegerField()
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')

    def __str__(self):
        return self.item_name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.item.item_name} ({self.quantity})"



class Aboutus(models.Model):
    description = models.TextField()
    
    def __str__(self):
        return self.description


class Feedback(models.Model):
    username = models.CharField(max_length=15)
    description = models.TextField(blank=False)
    rating = models.IntegerField()
    image = models.ImageField(upload_to='feedback_images/')

    def shortdesc(self, length=140):
        return (self.description[:length] + "...") if len(self.description) > length else self.description
    def __str__(self): 
        return self.username


class Booktable(models.Model):
    username =  models.CharField(max_length=15)
    phonenumber = models.CharField(max_length=20)
    email = models.EmailField()
    totalperson = models.IntegerField()
    bookingdate = models.DateField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/')

    def __str__(self):
        return ""


class Offer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='offers')
    percent = models.FloatField(default=0)
    image = models.ImageField(upload_to='offer_images/')

    def __str__(self):
        return "self.category"
    
