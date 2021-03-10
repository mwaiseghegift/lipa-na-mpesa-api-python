from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import MpesaPayment

import requests
from requests.auth import HTTPBasicAuth
import json
from .mpesa_credentials import MpesaAccessToken, LipaNaMpesaPassword
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def getAccessToken(request):
    consumer_key = 'n9KbDodntGKwIpwrENmqwghaXk18WstU'
    consumer_secret = 'TGxmOUSsa4FK4cuD'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    
    return HttpResponse(validated_mpesa_access_token)


def LipaNaMpesaOnline(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization":"Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipaNaMpesaPassword.business_short_code,
        "Password": LipaNaMpesaPassword.decode_password,
        "Timestamp": LipaNaMpesaPassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": f"{amount}",
        "PartyA": f"{telephone}",
        "PartyB": "174379",
        "PhoneNumber": f"{telephone}",
        "CallBackURL": "https://myhealthke.pythonanywhere.com/saf",
        "AccountReference": "MyHealth",
        "TransactionDesc": "myhealth test"
            }
            response = requests.post(api_url, json=request, headers=headers)
    print(response)
    return HttpResponse('success')

#register confirmation and validation url with safaricom
@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization":"Bearer %s" % access_token}
    options = {"ShortCode": LipaNaMpesaPassword.business_short_code,
               "ResponseType":"Completed",
               "ConfirmationUrl":"http://127.0.0.1:8000/c2b/confirmation",
               "ValidationUrl": "http://127.0.0.1:8000/c2b/validation",
               }
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

#capture the mpesa calls
@csrf_exempt
def call_back(request):
    pass

@csrf_exempt
def validation(request):
    context = {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    return JsonResponse(dict(context))

@csrf_exempt
def confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    
    payment = MpesaPayment (
        first_name = mpesa_payment['FirstName'],
        last_name = mpesa_payment['LastName'],
        middle_name = mpesa_payment['MiddleName'],
        description = mpesa_payment['TransID'],
        phone_number = mpesa_payment['MSISDN'],
        amount = mpesa_payment['TransAmount'],
        reference = mpesa_payment['BillRefNumber'],
        organization_balance = mpesa_payment['OrgAccountBalance'],
        type = mpesa_payment['TransactionType']
    )
    payment.save()
    context = {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    
    return JsonResponse(dict(context))