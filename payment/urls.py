from django.urls import path
from .views import stripe_config,create_checkout_session,cancelled

urlpatterns = [
  path('config/',stripe_config,name='stripe-config'),
  path('create-checkout-session/<str:vehicle_id>',create_checkout_session),
  path('cancelled/',cancelled,name='cancelled')
]
