from django.urls import path
from .views import (
    getAccessToken,
    LipaNaMpesaOnline,
    register_urls,
    call_back,
    validation,
    confirmation,
    simulate_transaction,
)

app_name = 'main'

urlpatterns = [
    path('access/token/', getAccessToken, name="get_mpesa_access_token"),
    path('online/lipa/', LipaNaMpesaOnline, name='lipa_na_mpesa'),
    path('c2b/register/', register_urls, name = "register"),
    path('c2b/callback/', call_back, name='callback'),
    path('c2b/validation/', validation, name="validation"),
    path('c2b/confirmation/', confirmation, name="confirmation"),
    path('c2b/simulate/', simulate_transaction, name='simulate') 
]
