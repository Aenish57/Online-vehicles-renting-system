
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Owner.models import Owner

from ClientHome.models import Customer
from Vehicles.models.vehicle import Vehicle
from RentVehicle.models import RentVehicle

from datetime import datetime
from datetime import date
import os
from urllib.request import Request
import requests
import re
from VehicleRentingSystem.settings import MEDIA_ROOT

# Create your views here.
def index(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    vehicle = Vehicle.objects.all()
    Message="Welcome Aboard!!"
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Owner_index.html',{'vehicle':vehicle,'Message':Message,'owner':owner,'no_of_pending_request':no_of_pending_request})

def Profile(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Owner_Profile.html',{'owner':owner,'no_of_pending_request':no_of_pending_request})

def vehicle_map(request):
    response = requests.get('http://ip-api.com/json/')
    data = response.json()
    print(data)
    return render(request,'vehicle_map.html',{'lat':data['lat'],'lon':data['lon']})


def AllCustomers(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    customer = Customer.objects.all()
    no_of_pending_request=count_pending_rent_request()
    return render(request,"All_Customers.html",{'customer':customer,'owner':owner,'no_of_pending_request':no_of_pending_request})



def Customer_Profile(request,customer_email):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    customer = Customer.objects.get(customer_email=customer_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Owner_Customer_Profile.html',{'owner':owner,'customer':customer,'no_of_pending_request':no_of_pending_request})

def upload_Vehicle(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,"Owner_Upload_Vehicle.html",{'owner':owner,'no_of_pending_request':no_of_pending_request})

def AllVehicles(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    vehicle = Vehicle.objects.all()
    no_of_pending_request=count_pending_rent_request()
    return render(request,"Owner_all_vehicles.html",{'vehicle':vehicle,'owner':owner,'no_of_pending_request':no_of_pending_request})

def showdetails(request,Vehicle_license_plate):
    if('user_email' not in request.session):
        return redirect('/signin/')
    vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)
    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Owner_showdetails.html',{'vehicle':vehicle,'owner':owner,'no_of_pending_request':no_of_pending_request})

def CheckAvailability(request,Vehicle_license_plate):
    if('user_email' not in request.session):
        return redirect('/signin/')

    RentVehicle_Date_of_Booking=request.POST.get('RentVehicle_Date_of_Booking','')
    RentVehicle_Date_of_Return=request.POST.get('RentVehicle_Date_of_Return','')

    RentVehicle_Date_of_Booking = datetime.strptime(RentVehicle_Date_of_Booking, '%Y-%m-%d').date()
    RentVehicle_Date_of_Return = datetime.strptime(RentVehicle_Date_of_Return, '%Y-%m-%d').date()

    rentvehicle = RentVehicle.objects.filter(Vehicle_license_plate=Vehicle_license_plate)
    vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)

    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)

    no_of_pending_request=count_pending_rent_request()

    if RentVehicle_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request,'Owner_showdetails.html',{'Incorrect_dates':Incorrect_dates,'vehicle':vehicle,'owner':owner,'no_of_pending_request':no_of_pending_request})

    if RentVehicle_Date_of_Return < RentVehicle_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request,'Owner_showdetails.html',{'Incorrect_dates':Incorrect_dates,'vehicle':vehicle,'owner':owner,'no_of_pending_request':no_of_pending_request})
    
    days=(RentVehicle_Date_of_Return-RentVehicle_Date_of_Booking).days+1
    total=days*vehicle.Vehicle_price
    
    rent_data = {"RentVehicle_Date_of_Booking":RentVehicle_Date_of_Booking, "RentVehicle_Date_of_Return":RentVehicle_Date_of_Return,"days":days, "total":total}
    
    for rv in rentvehicle:

        # if (RentVehicle_Date_of_Booking < rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return < rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking > rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return > rv.RentVehicle_Date_of_Return):
        #     Available = True
        #     return render(request,'Owner_showdetails.html',{'Available':Available,'vehicle':vehicle,'owner':owner,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})

        if (rv.RentVehicle_Date_of_Booking >= RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return >= rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking >= rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return <= rv.RentVehicle_Date_of_Return) or (RentVehicle_Date_of_Booking <= rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return >= rv.RentVehicle_Date_of_Return):
            if rv.isAvailable:
                Available = True
                Message = "Note that somebody has also requested for this vehicle from " + str(rv.RentVehicle_Date_of_Booking) + " to " + str(rv.RentVehicle_Date_of_Return)
                return render(request,'Owner_showdetails.html',{'Message':Message,'Available':Available,'vehicle':vehicle,'owner':owner,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})

            NotAvailable = True
            return render(request,'Owner_showdetails.html',{'NotAvailable':NotAvailable,'dates':rv,'vehicle':vehicle,'owner':owner,'no_of_pending_request':no_of_pending_request})
    
    Available = True
    return render(request,'Owner_showdetails.html',{'Available':Available,'vehicle':vehicle,'owner':owner,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})

def RentRequest(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)

    rentvehicle = RentVehicle.objects.all()
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Owner_RentRequest.html',{'owner':owner,'rentvehicle':rentvehicle,'no_of_pending_request':no_of_pending_request})

def SentRequests(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    owner_email = request.session.get('user_email')
    owner = Owner.objects.get(Owner_email=owner_email)

    no_of_pending_request=count_pending_rent_request()

    rentvehicle = RentVehicle.objects.filter(customer_email=owner_email)
    if rentvehicle.exists():
        vehicle = Vehicle.objects.all()
        return render(request,'Owner_SentRequests.html',{'owner':owner,'rentvehicle':rentvehicle,'vehicle':vehicle,'no_of_pending_request':no_of_pending_request})
    else:
        Message = "You haven't rented any vehicle yet!!"
        return render(request,'Owner_SentRequests.html',{'owner':owner,'rentvehicle':rentvehicle,'Message':Message,'no_of_pending_request':no_of_pending_request})



def DeleteVehicle(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    Vehicle_license_plate = request.GET.get('Vehicle_license_plate','')
    vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)

    path1 = MEDIA_ROOT + str(vehicle.Vehicle_image1)
    path2 = MEDIA_ROOT + str(vehicle.Vehicle_image2)
    path3 = MEDIA_ROOT + str(vehicle.Vehicle_image3)

    os.remove(path1)
    os.remove(path2)
    os.remove(path3)

    vehicle.delete()
    

    return redirect('/Owner/AllVehicles/')

def count_pending_rent_request():
    no_of_pending_request=0
    rentvehicle = RentVehicle.objects.all()
    for rv in rentvehicle:
        if rv.request_status == "Pending":
            no_of_pending_request+=1
    return no_of_pending_request