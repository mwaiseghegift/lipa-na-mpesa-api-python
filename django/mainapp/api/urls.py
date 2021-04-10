from django.urls import path
from mainapp.api.views import *

app_name = 'api'

urlpatterns = [
    path('access/token/', getAccessToken, name="api_get_mpesa_access_token"),
    path('online/lipa/', LipaNaMpesaOnline, name='api_lipa_na_mpesa'),
    path('c2b/register/', register_urls, name = "api_register"),
    path('c2b/callback/', call_back, name='api_callback'),
    path('c2b/validation/', validation, name="api_validation"),
    path('c2b/confirmation/', confirmation, name="api_confirmation"),
    path('c2b/simulate/', simulate_transaction, name='api_simulate') 
]
