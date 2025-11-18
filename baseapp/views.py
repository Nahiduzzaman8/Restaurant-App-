from django.shortcuts import render
from .models import *
from django.http import HttpResponse

# Create your views here.
def Home(request):
    offers = Offer.objects.all()
    sliders = SliderImage.objects.all()
    category = Category.objects.all()[:3]
    items = Items.objects.all()[:6]
    return render(request, 'home.html', {
        'sliders':sliders,
        'offers':offers, 
        'category':category,
        'items':items
    })

def About(request):
    return render(request, 'about.html')

def Menu(request):
    cats = Category.objects.all()
    items = Items.objects.all()
    return render(request, 'menu.html', {
        'cats':cats,
        'items':items
    })

def Book_Table(request):
    return render(request, 'book_table.html')

def Feedback_Form(request):
    return render(request, 'feedback.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'login.html')


def logout(request):
    return render(request, 'login.html')


    
    