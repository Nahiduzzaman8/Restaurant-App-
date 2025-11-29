from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from baseapp import views
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='Home'),
    path('about/', views.About, name='About'),
    path('menu/', views.Menu, name='Menu'),
    path('booktable/', views.Book_Table, name='Book_Table'),
    path('feedback/', views.Feedback_Form, name='Feedback_Form'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    # path('cartitems/', views.cartitems, name='cartitems') 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
