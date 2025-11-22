from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def Home(request):
    offers = Offer.objects.all()
    sliders = SliderImage.objects.all()
    category = Category.objects.all()[:3]
    items = Items.objects.all()[:6]
    feedbacks = Feedback.objects.all() 
    return render(request, 'home.html', {
        'sliders':sliders,
        'offers':offers, 
        'category':category,
        'items':items, 
        'feedbacks':feedbacks
    })


def About(request):
    about = Aboutus.objects.last()
    return render(request, 'about.html',{
        'about':about
    })


def Menu(request):
    cats = Category.objects.all()
    items = Items.objects.all()
    return render(request, 'menu.html', {
        'cats':cats,
        'items':items
    })


def Book_Table(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            phonenumber = request.POST.get('phonenumber')
            email = request.POST.get('email')
            totalperson = int(request.POST.get('totalperson'))
            bookingdate = request.POST.get('bookingdate')
            print(username, phonenumber, email, totalperson, bookingdate)
            booktable = Booktable.objects.create(username=username, 
                                            phonenumber= phonenumber, 
                                            email= email, 
                                            totalperson= totalperson, 
                                            bookingdate=bookingdate)
            # booktable.save() maybe not need. as 'create' may save it already
        except Exception as e:
                messages.error(request, f"Something went wrong: {str(e)}")
        else:
            messages.success(request, "Information taken. We will reach you in a while!!")
            return redirect('Book_Table')
    return render(request, 'book_table.html')


def Feedback_Form(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            experience = request.POST.get('experience')
            rating = request.POST.get('rating')
            image = request.FILES.get('image')
            feedback = Feedback.objects.create(username=username, 
                                            description= experience, 
                                            rating= rating, 
                                            image= image)
            feedback.save() #maybe not need. as 'create' may save it already
        except Exception as e:
                messages.error(request, f"Something went wrong: {str(e)}")
        else:
            messages.success(request, "Feedback taken!!")
            return redirect('Feedback_Form')

    return render(request, 'feedback.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'login.html')


# def logout(request):
#     return render(request, 'login.html')

