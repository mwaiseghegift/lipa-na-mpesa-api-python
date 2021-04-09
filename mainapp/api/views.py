from rest_framework.decorators import api_view
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from mainapp.models import MpesaPayment

import requests
from requests.auth import HTTPBasicAuth
import json
from mainapp.mpesa_credentials import MpesaAccessToken, LipaNaMpesaPassword
from django.views.decorators.csrf import csrf_exempt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import os


# Create your views here.

def getAccessToken(request):
    consumer_key = 'bs84aD7VaJLrZosruylv9dAGi1dYnuJy'
    consumer_secret = 'UcgJr2x3xwlHg3GK'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    
    return HttpResponse(validated_mpesa_access_token)

@api_view(['POST'])
def LipaNaMpesaOnline(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization":"Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipaNaMpesaPassword.business_short_code,
        "Password":LipaNaMpesaPassword.decode_password,
        "Timestamp":LipaNaMpesaPassword.lipa_time,
        "TransactionType":"CustomerPayBillOnline",
        "Amount":"5",
        "PartyA":"254712860997",
        "PartyB":"174379",
        "PhoneNumber":"254712860997",
        "CallBackURL":"https://myhealthke.pythonanywhere.com/saf",
        "AccountReference":"GiftWasHere",
        "TransactionDesc":"myhealth test"
            }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')

#register confirmation and validation url with safaricom
@api_view(['GET'])
@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipaNaMpesaPassword.test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://3776411096cb.ngrok.io/c2b/confirmation/",
               "ValidationURL": "https://3776411096cb.ngrok.io/c2b/validation/"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

#simulate transaction
@api_view(['POST'])
@csrf_exempt
def simulate_transaction(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = { "ShortCode":"600383",
                "CommandID":"CustomerPayBillOnline",
                "Amount":"50",
                "Msisdn":"254708374149",
                "BillRefNumber":LipaNaMpesaPassword.business_short_code }
  
    response = requests.post(api_url, json = request, headers=headers)
    return HttpResponse(response.text)


#capture the mpesa calls
@csrf_exempt
def call_back(request):
    pass

@csrf_exempt
def validation(request):
    
    data = json.loads(request.body)
    file = open('validate.json','a')
    file.write(json.dumps(data))
    file.close()
    
    context = {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    return JsonResponse(dict(context))

@csrf_exempt
def confirmation(request):
    data = json.loads(request.body)
    file = open('validate.json','a')
    file.write(json.dumps(data))
    file.close()
    
    # mpesa_body = request.body.decode('utf-8')
    # mpesa_payment = json.loads(mpesa_body)
    
    # payment = MpesaPayment (
    #     first_name=mpesa_payment['FirstName'],
    #     last_name=mpesa_payment['LastName'],
    #     middle_name=mpesa_payment['MiddleName'],
    #     description=mpesa_payment['TransID'],
    #     phone_number=mpesa_payment['MSISDN'],
    #     amount=mpesa_payment['TransAmount'],
    #     reference=mpesa_payment['BillRefNumber'],
    #     organization_balance=mpesa_payment['OrgAccountBalance'],
    #     type=mpesa_payment['TransactionType']
    # )
    # payment.save()
    context = {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    
    return JsonResponse(dict(context))