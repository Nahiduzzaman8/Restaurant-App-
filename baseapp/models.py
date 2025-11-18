from django.db import models

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

class Aboutus(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description
    
class Feedback(models.Model):
    username = models.CharField(max_length=15)
    description = models.TextField(blank=False)
    rating = models.IntegerField()

    def __str__(self):
        return self.username
    
class Booktable(models.Model):
    name =  models.CharField(max_length=15)
    phone_number = models.IntegerField()
    email = models.EmailField()
    total_person = models.IntegerField()
    booking_data = models.DateField()

    
    def __str__(self):
        return self.name

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
