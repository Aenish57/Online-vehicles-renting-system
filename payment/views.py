import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import redirect, render
from ClientHome.models import Customer
from Vehicles.models.vehicle import Vehicle
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
@csrf_exempt
def stripe_config(request):
  if request.method == 'GET':
    config = {'publicKey':settings.STRIPE_PUBLISHABLE_KEY}
    return JsonResponse(config,safe=False)

@csrf_exempt
def create_checkout_session(request,vehicle_id):
    print(request.user)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        
                        'name': vehicle.name,
                        'quantity': 1,
                        'currency': 'usd',
                        
                        'amount': int(vehicle.price),
                        'description':vehicle.description,
                        
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
def cancelled(request):
  return render(request,'payments/cancelled.html')