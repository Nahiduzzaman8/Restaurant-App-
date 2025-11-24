from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from . import jwt_utils

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

        # Extract data
        username = request.POST.get('username')
        phonenumber = request.POST.get('phonenumber')
        email = request.POST.get('email')
        totalperson = request.POST.get('totalperson')
        bookingdate = request.POST.get('bookingdate')

        # -----------------------
        # START VALIDATION BLOCK
        # -----------------------

        # 1. Username
        if not username or len(username) < 3:
            messages.error(request, "Please enter a valid name.")
            return redirect('Book_Table')

        # 2. Phone Number
        if not phonenumber.isdigit() or len(phonenumber) < 10:
            messages.error(request, "Please enter a valid phone number.")
            return redirect('Book_Table')

        # 3. Email format
        try:
            validate_email(email)
        except ValidationError as exp:
            messages.error(request, "Please enter a valid email.", exp)
            return redirect('Book_Table')

        # 4. Total Person
        try:
            totalperson = int(totalperson)
            if totalperson <= 0:
                raise ValueError
        except:
            messages.error(request, "Total person must be a positive number.")
            return redirect('Book_Table')

        # 5. Booking Date
        if not bookingdate:
            messages.error(request, "Please choose a booking date.")
            return redirect('Book_Table')

        # -----------------------
        # END VALIDATION BLOCK
        # -----------------------

        # Create record if everything is valid
        try:
            Booktable.objects.create(
                username=username,
                phonenumber=phonenumber,
                email=email,
                totalperson=totalperson,
                bookingdate=bookingdate
            )
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        else:
            messages.success(request, "Information taken. We will reach you in a while!!")
            return redirect('Book_Table')
    
    return render(request, 'book_table.html')


def Feedback_Form(request):
    if request.method == "POST":

        # Extract form data
        username = request.POST.get('username')
        experience = request.POST.get('experience')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')

        # -----------------------
        # VALIDATION BLOCK
        # -----------------------

        # 1. Username Validation
        if not username or len(username) < 3:
            messages.error(request, "Please provide a valid username (min 3 characters).")
            return redirect('Feedback_Form')

        # 2. Experience Validation
        if not experience:
            messages.error(request, "Experience can not be empty.")
            return redirect('Feedback_Form')

        # 3. Rating validation
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except:
            messages.error(request, "Rating must be a number between 1 and 5.")
            return redirect('Feedback_Form')

        # 4. Image validation (optional)
        if image:
            if not image.content_type in ['image/jpeg', 'image/png']:
                messages.error(request, "Only JPEG or PNG images are allowed.")
                return redirect('Feedback_Form')

            if image.size > 2 * 1024 * 1024:  # 2 MB
                messages.error(request, "Image size cannot exceed 2MB.")
                return redirect('Feedback_Form')

        # -----------------------
        # END VALIDATION BLOCK
        # -----------------------

        # Save data only if all validations pass
        try:
            Feedback.objects.create(
                username=username,
                description=experience,
                rating=rating,
                image=image
            )
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        else:
            messages.success(request, "Feedback taken!!")
            return redirect('Feedback_Form')

    return render(request, 'feedback.html')

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


def signup(request):
    return render(request, 'login.html')


def logout(request):
    return render(request, 'login.html')

from django.contrib import messages
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        #authenticate
        user = authenticate(username=username, password=password)

        #checking user
        if user is None:  
            return render(request, "login.html", {
                "messages":"Invalid Credentials"
            })   
        if user.is_superuser:
            return redirect('/admin/') 
        
        #generete token
        token = jwt_utils.create_jwt(user.id)
        print(token)

        response = redirect('Home')
        response.set_cookie('token', token, httponly=True ) # set the token into cookie
        return response
    
        # return JsonResponse({     #JSON response (JsonResponse) is for APIs. 
        #     "status":"success",   #For regular HTML forms, redirect + cookie is the usual pattern.
        #     "message":"token genereted successfully",    
        #     "token":token
        # }, status=200)
    
    return render(request, 'login.html')


def cartitems(request):
    user = jwt_utils.decode_jwt(request)
    if not user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    items = Items.objects.filter(user=user)
    data = [
        {
            "name": item.item_name,
            "category": item.category,
            "price": item.price
        } for item in items
    ]

    return JsonResponse({"items": data})

