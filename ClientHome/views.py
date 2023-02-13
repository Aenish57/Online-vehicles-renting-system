from urllib.request import Request
from http import server
import smtplib
from telnetlib import SE

from django.core.mail import send_mail
import math, random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from ClientHome.models import Customer
from Owner.models import Owner

#from Owner.templates import Owner_upload_vehicle

from Vehicles.models.vehicle import Vehicle
from Vehicles.models.category import Category
from RentVehicle.models import RentVehicle

from datetime import datetime
from datetime import date
import hashlib

#defining function to send email
def send_email(to:str,subject:str,body:str):
    SENDER_EMAIL = getattr(settings,'EMAIL_HOST_USER')
    SENDER_PASSWORD = getattr(settings,'EMAIL_HOST_PASSWORD')
    try:
        
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL,SENDER_PASSWORD)
        email_text = f"""
            From {SENDER_EMAIL}
            To {to}
            Subject {subject}
            {body}
        """
        server.sendmail(SENDER_EMAIL,to,email_text)
        print(f'EMAIL SENT TO {to}')
    except Exception as error:
        print(error)

isLogin = False
isLogout = False

# Create your views here.
# def Home(request):
#     global isLogin
#     global isLogout
#     vehicle = Vehicle.objects.all()
#     categories = Category.get_all_categories();
#     data = {}
#     data['vehicle'] = vehicle
#     data['category'] = categories

#     return render(request , 'Home.html' , data)
#Rendering main page
def index(request):
    global isLogin
    global isLogout

    if('user_email' in request.session):
        email = request.session.get('user_email')

        result_customer = Customer.objects.filter(customer_email=email)
        result_owner = Owner.objects.filter(Owner_email=email)
        

        if result_customer.exists():
            request.session['user_email'] = email
            isLogin = True
            return redirect('/Home/')
        elif result_owner.exists():
            request.session['user_email'] = email
            isLogin = True
            return redirect('/Owner/')
        return redirect('/Home/')
       

    vehicle = Vehicle.objects.all()
    if('user_email' not in request.session and isLogout):
        isLogin = False
        isLogout = False
        Message = "You have been Logged Out"
        return render(request,'index.html',{'Message':Message,'vehicle':vehicle})
    return render(request,'index.html',{'vehicle':vehicle})

#Rendering login page
def LoginAuthentication(request):
    global isLogin
    login_email=request.POST.get('login_email','')
    login_password=request.POST.get('login_password','')
    #customer = Customer.objects.all()

    login_password_hash=hashlib.sha224(login_password.encode()).hexdigest()
    result_customer = Customer.objects.filter(customer_email=login_email,customer_password=login_password_hash)
    result_owner = Owner.objects.filter(Owner_email=login_email,Owner_password=login_password)
    

    if result_customer.exists():
        request.session['user_email'] = login_email
        isLogin = True
        return redirect('/Home/')
    elif result_owner.exists():
        request.session['user_email'] = login_email
        isLogin = True
        return redirect('/Owner/')
   
    else:
        Message = "Email or password is invalid"
        return render(request,'SignIn.html',{'Message':Message})
#Rendering registrattion page
def RegisterCustomer(request):
    global isLogin

    customer_firstname=request.POST.get('customer_firstname','')
    customer_lastname=request.POST.get('customer_lastname','')
    customer_dob=request.POST.get('customer_dob','')
    customer_gender=request.POST.get('customer_gender','')
    customer_mobileno=request.POST.get('customer_mobileno','')
    customer_email=request.POST.get('customer_email','')


    
    customer_password=request.POST.get('customer_password','')

    customer_password_hash=hashlib.sha224(customer_password.encode()).hexdigest()
    print(customer_password_hash)
    
    customer_address=request.POST.get('customer_address','')
    customer_city=request.POST.get('customer_city','')
    customer_state=request.POST.get('customer_state','')
    customer_country=request.POST.get('customer_country','')
    
    customer_license=request.FILES['customer_license']

    result_customer = Customer.objects.filter(customer_email=customer_email)
    result_owner = Owner.objects.filter(Owner_email=customer_email)
    
    if result_customer.exists() or result_owner.exists() :
        Message = "This Email address has been already used"
        return render(request,'register.html',{'Message':Message})
    else:
        customer=Customer(customer_firstname=customer_firstname,customer_lastname=customer_lastname,
        customer_dob=customer_dob,customer_gender=customer_gender,customer_mobileno=customer_mobileno,
        customer_email=customer_email,customer_password=customer_password_hash,customer_address=customer_address,
        customer_city=customer_city,customer_country=customer_country,
        customer_license=customer_license)
        
        customer.save()
        request.session['user_email'] = customer_email
        send_email(customer_email,'Please verify your account','Please follow the link below to verify your account.http://localhost:8000/verify-account')
        isLogin = True
        return redirect('/Home/')


def about(request):
    return render(request, 'about.html')

def signin(request):
    return render(request,'SignIn.html')

def register(request):
    return render(request,'register.html')

def term(request):
    return render(request,'terms.html')

def password_reset_form(request):
    return render(request,'pasword_reset_form.html')

def Logout(request):
    global isLogout
    del request.session['user_email']
    isLogout = True
    Message = "You have been Logged Out"
    return redirect('/')

def contact_us(request):
    return render(request,'contact_us.html')

# def generateOTP() :
#      digits = "0123456789"
#      OTP = ""
#      for i in range(4) :
#          OTP += digits[math.floor(random.random() * 10)]
#      return OTP
# def send_otp(request):
#      email=request.GET.get   ("email")
#      print(email)
#      o=generateOTP()
#      htmlgen = '<p>Your OTP is <strong>o</strong></p>'
#      send_mail('OTP request',o,'<your gmail id>',[email], fail_silently=False, html_message=htmlgen)
#      return HttpResponse(o)


#Rendering to Home page afte login

def Home(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)
    vehicle = Vehicle.objects.all()
    categories = Category.objects.all()
    Message="Welcome "
    return render(request,'Home.html',{'vehicle':vehicle,'categories':categories,'Message':Message,'customer':customer})

def Profile(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)
    return render(request,'Profile.html',{'customer':customer})

def showdetails(request,Vehicle_license_plate):
    vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)
    if('user_email' not in request.session):
        return render(request,'showdetails_not_login.html',{'vehicle':vehicle})
    else:
        customer_email = request.session.get('user_email')
        customer = Customer.objects.get(customer_email=customer_email)
        return render(request,'showdetails_loggedin.html',{'vehicle':vehicle,'customer':customer})

#Checking wheathe the car is available or not in booking date.
def CheckAvailability(request,Vehicle_license_plate):
    if('user_email' not in request.session):
        return redirect('/signin/')

    RentVehicle_Date_of_Booking=request.POST.get('RentVehicle_Date_of_Booking','')
    RentVehicle_Date_of_Return=request.POST.get('RentVehicle_Date_of_Return','')
    
    RentVehicle_Date_of_Booking = datetime.strptime(RentVehicle_Date_of_Booking, '%Y-%m-%d').date()
    RentVehicle_Date_of_Return = datetime.strptime(RentVehicle_Date_of_Return, '%Y-%m-%d').date()

    rentvehicle = RentVehicle.objects.filter(Vehicle_license_plate=Vehicle_license_plate)
    vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)

    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)

    if RentVehicle_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request,'showdetails_loggedin.html',{'Incorrect_dates':Incorrect_dates,'vehicle':vehicle,'customer':customer})

    if RentVehicle_Date_of_Return < RentVehicle_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request,'showdetails_loggedin.html',{'Incorrect_dates':Incorrect_dates,'vehicle':vehicle,'customer':customer})
    
    days=(RentVehicle_Date_of_Return-RentVehicle_Date_of_Booking).days+1
    total=days*vehicle.Vehicle_price
    
    rent_data = {"RentVehicle_Date_of_Booking":RentVehicle_Date_of_Booking, "RentVehicle_Date_of_Return":RentVehicle_Date_of_Return,"days":days, "total":total}
    #Geting the list of all vehicles from the database
    for rv in rentvehicle:
        #Checkig wheather the car user is trying to book is already booked or not
        if (rv.RentVehicle_Date_of_Booking >= RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return >= rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking >= rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return <= rv.RentVehicle_Date_of_Return) or (RentVehicle_Date_of_Booking <= rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return >= rv.RentVehicle_Date_of_Return):
            if rv.isAvailable:
                Available = True
                Message = "Note that somebody has also requested for this vehicle from " + str(rv.RentVehicle_Date_of_Booking) + " to " + str(rv.RentVehicle_Date_of_Return)
                return render(request,'showdetails_loggedin.html',{'Message':Message,'Available':Available,'vehicle':vehicle,'customer':customer,'rent_data':rent_data})

            NotAvailable = True
            return render(request,'showdetails_loggedin.html',{'NotAvailable':NotAvailable,'dates':rv,'vehicle':vehicle,'customer':customer})

        # if (RentVehicle_Date_of_Booking < rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return < rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking > rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return > rv.RentVehicle_Date_of_Return):
        #     Available = True
        #     return render(request,'showdetails_loggedin.html',{'Available':Available,'vehicle':vehicle,'customer':customer,'rent_data':rent_data})


    Available = True
    #Displaying and alert about the status of renting.
    return render(request,'showdetails_loggedin.html',{'Available':Available,'vehicle':vehicle,'customer':customer,'rent_data':rent_data})

def SentRequests(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    customer_email = request.session.get('user_email')
    customer = Customer.objects.get(customer_email=customer_email)

    rentvehicle = RentVehicle.objects.filter(customer_email=customer_email)
    if rentvehicle.exists():
        vehicle = Vehicle.objects.all()
        return render(request,'SentRequests.html',{'customer':customer,'rentvehicle':rentvehicle,'vehicle':vehicle})
    else:
        Message = "You haven't rented any vehicle yet"
        return render(request,'SentRequests.html',{'customer':customer,'rentvehicle':rentvehicle,'Message':Message})

def search(request:Request):
    filtered_vehicles = []
    if request.method == 'POST':
        search_query = request.POST.get('q')
        category = Category.objects.filter(name=search_query)[0]
        categories = Category.objects.all()
        print(category)
        filtered_vehicles = Vehicle.objects.filter(category=category)
    return render(request, 'search.html',{'vehicle':filtered_vehicles,'categories':categories})
    
