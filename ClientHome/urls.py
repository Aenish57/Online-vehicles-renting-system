from django.contrib import admin
from django.urls import path
from . import views
#from django.conf.urls import url
#from django.
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="Home"),
    # path('<slug:category_slug>', views.index, name='vehicle_by_category'),
    #path("send_otp",views.send_otp,name="send otp"),
    # path('accounts/', include('django.contrib.auth.urls')),

    #path('pattern, Calling function name, name of function)
    path('<int:id>/', views.Home, name='Home'),
    path('Home/', views.Home, name="LoggedinHome"),
    path('signin/',views.signin,name="SignIn"),
    path('Logout/',views.Logout,name="Logout"), 

    
       
    path('register/',views.register,name="Register"),
    path('Profile/',views.Profile,name="Profile"),
    path('about/', views.about, name="about"),
    path('terms/', views.term, name="term"),
    path('contact/', views.contact_us, name="contact_us"),
    path('search/', views.search, name="Search"),
    path('LoginAuthentication/',views.LoginAuthentication,name="LoginAuthentication"),
    path('RegisterCustomer/',views.RegisterCustomer,name="RegisterCustomer"),
    path('VehicleDetails/<str:Vehicle_license_plate>/',views.showdetails,name="VehicleDetails"),
    path('CheckAvailability/<str:Vehicle_license_plate>/',views.CheckAvailability,name="CheckAvailability"),
    path('SentRequests/',views.SentRequests,name="SentRequests"),
    
    path('RentVehicle',include("RentVehicle.urls")),
    path('Owner/',include("Owner.urls")),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
      name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
]
#default path of statics files.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)