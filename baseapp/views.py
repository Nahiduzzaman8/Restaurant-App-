from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from . import jwt_utils
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
import jwt
import datetime
from django.conf import settings
import json

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
    contactus = ContactUs.objects.last()
    sociallinks = SocialMedia.objects.last()
    opening_hours = Opening_Hours.objects.last()

    return render(request, 'about.html',{
        'about':about,
        'contactus': {
            "location":contactus.location,
            "number":contactus.number,
            "email":contactus.email,

        },
        'sociallinks': {
            "facebook":sociallinks.facebook,
            "twitter":sociallinks.twitter,
            "linkedin":sociallinks.linkedin,
            "instagram":sociallinks.instagram,
            "pinterest":sociallinks.pinterest,

        },
        'opening_hours': {
            "opening_day":opening_hours.opening_day,
            "opening_time":opening_hours.opening_time
        }
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


def logout(request):
    response = redirect("login")
    response.delete_cookie("access") 

    return response


@ratelimit(key='ip', rate='5/h', method='POST', block=True)
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Manual validations
        if len(username) < 3:
            messages.error(request, "Username must be at least 3 characters long.")
            return redirect('signup')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Account created successfully.")
        return redirect('login')

    # For GET requests
    return render(request, 'login.html')


@csrf_exempt
@ratelimit(key='ip', rate='5/h', method='POST', block=True)
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #authenticate
        user = authenticate(username=username, password=password)
        
        #checking user
        if user is None:  
            return render(request, "login.html", {"error": "Invalid credentials"})
        
        payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
        }
        token = jwt_utils.create_jwt(user)
        response = redirect("Home")  # THIS REDIRECTS TO HOME

        # Set JWT inside HttpOnly cookie
        response.set_cookie(
        key="access",
        value=token,
        httponly=False,
        secure=False,        # True in production (HTTPS)
        samesite="Strict",   # Prevent CSRF
        max_age=3600,
        )

        return response
    
    return render(request, 'login.html')


def add_to_cart(request):
    if request.method != "POST":
        return JsonResponse({
            "message":"Invalid method"
        }, status=400)
    
    token = request.COOKIES.get('access')
    if not token :
        return JsonResponse({
            "message":"Not logged in"
        }, status=401)
    
    payload = jwt_utils.decode_jwt(token)
    if not payload:
        return JsonResponse({
            "message": "Invalid token"
        }, status=401)

    user_id = payload['user_id']
    user = User.objects.get(id=user_id)
    body = json.loads(request.body)

    item_id = body['item_id']
    if not item_id:
        return JsonResponse({
            "message": "item_id required"
        },status=400)
    
    item = Items.objects.get(id=item_id)

    # 4. Get/create user cart
    cart, created = Cart.objects.get_or_create(user=user)

    # 5. Check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({
    "message": "Item added to cart successfully",
    # "item_id": body["item_id"]
})
    

def get_cart_items(request):
    # 1. JWT from cookie
    token = request.COOKIES.get("access")
    if not token:
        return JsonResponse({"error": "Not logged in"}, status=401)

    # 2. decode
    payload = jwt_utils.decode_jwt(token)
    if payload is None:
        return JsonResponse({"error": "Invalid token"}, status=401)
    
    user_id = payload["user_id"]
    user = User.objects.get(id=user_id)

    # 3. Get the user's cart
    cart, created = Cart.objects.get_or_create(user=user)

    # 4. Build response data
    data = []
    for item in cart.items.all():
        data.append({
            "name": item.item.item_name,
            "price": item.item.price,
            "quantity": item.quantity,
            "total": item.item.price * item.quantity,
            "image": item.item.image.url
        })

    return JsonResponse({"items": data})

