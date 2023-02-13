from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from ClientHome import views as cust_views
from Vehicles import views as veh_views
from .views import vehicle_map

urlpatterns = [
    path('', views.index, name="Owner"),
    path('vehicle_map',vehicle_map,name='vehicle_map'),
    path('signin/',cust_views.signin, name="SignIn"),
    path('Logout/',cust_views.Logout, name="Logout"),
    path('Profile/',views.Profile, name="Profile"),
    path('UploadVehicle/',views.upload_Vehicle, name="UploadVehicle"),
   
    path('AllCustomers/',views.AllCustomers, name="AllCustomers"),
    path('AllVehicles/',views.AllVehicles, name="AllVehicles"),
    path('VehicleDetails/<str:Vehicle_license_plate>/',views.showdetails,name="OwnerVehicleDetails"),
    path('CheckAvailability/<str:Vehicle_license_plate>/',views.CheckAvailability,name="OwnerCheckAvailability"),
    path('RentRequest/',views.RentRequest,name="RentRequest"),
    path('SentRequests/',views.SentRequests,name="SentRequests"),
   
    path('DeleteVehicle/',views.DeleteVehicle,name="DeleteVehicle"),
    
    path('CustomerProfile/<str:customer_email>/',views.Customer_Profile,name="CustomerProfile"),
    path('Vehicle/UploadVehicle',veh_views.upload_vehicle,name="UploadVehicle")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)