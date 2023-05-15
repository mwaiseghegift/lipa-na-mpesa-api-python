import time
import math
import base64
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
from decouple import config

import time
import math
import base64
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
from decouple import config
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .mpesa_credentials import MpesaAccessToken, LipaNaMpesaPassword

class MpesaHandler:
    now = None
    shortcode = None
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    access_token = None
    access_token_expiration = None
    stk_push_url = None
    my_callback_url = None
    query_status_url = None
    timestamp = None
    passkey = None

    def __init__(self):
        """ initializing payment objects """
        self.now = datetime.now()
        self.shortcode = config("MPESA_SHORTCODE")
        self.consumer_key = config("MPESA_CONSUMER_KEY")
        self.consumer_secret = config("MPESA_CONSUMER_SECRET")
        self.access_token_url = config("access_token_url")
        self.passkey = config("MPESA_PASSKEY")
        self.stk_push_url = config("SAF_STK_PUSH_API")
        self.query_status_url = config("SAF_STK_PUSH_QUERY_API")
        self.my_callback_url = config("c2b_callback")
        self.validation_url = config("validation_url")
        self.confirmation_url = config("confirmation_url")
        self.password = self.generate_password()


        try:
            self.access_token = self.get_mpesa_access_token()
            if self.access_token is None:
                raise Exception("Request for access token failed")
            else:
                self.access_token_expiration = time.time() + 3599
        except Exception as e:
            # log this errors 
            print(str(e))


    def get_mpesa_access_token(self):
        """ get access token from safaricom mpesa"""
        try:
            res = requests.get(
                self.access_token_url,auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
            )
            token = res.json()['access_token']
            self.headers = {"Authorization": f"Bearer {token}","Content-Type": "application/json" }
        except Exception as e:
            print(str(e), "error from get access token")
            raise e
        return token


    def generate_password(self):
        """ generate a password for the api using shortcode and passkey """
        self.timestamp = self.now.strftime("%Y%m%d%H%M%S")
        password_str = self.shortcode + self.passkey + self.timestamp
        password_bytes = password_str.encode()
        return base64.b64encode(password_bytes).decode("utf-8")


    def make_stk_push(self, payload):
        """ push payment request to the mpesa no."""
        amount = payload['amount']
        phone_number = payload['phone_number']

        push_data = {
            "BusinessShortCode": self.shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.my_callback_url,
            "AccountReference": "Journaling Therapy",
            "TransactionDesc": "journaling transaction test",
        }

        response = requests.post(self.stk_push_url, json=push_data, headers=self.headers)
        response_data = response.json()

        return response_data

    def query_transaction_status(self, checkout_request_id):
        """ query the status of the transaction."""
        query_data = {
            "BusinessShortCode": self.shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        response = requests.post(self.query_status_url, json=query_data, headers=self.headers)
        response_data = response.json()
        

        return response_data
    
    def register_c2b_url(self):
        """ register the callback url with safaricom """
        payload = {
            "ShortCode": self.shortcode,
            "ResponseType": "Completed",
            "ConfirmationURL": self.confirmation_url,
            "ValidationURL": self.validation_url
        }

        response = requests.post(self.register_url, json=payload, headers=self.headers)
        response_data = response.json()

        return response_data



# make payment
def stk_push(request):
    amount = "1"
    phone_number = "254712860997"
    payload = {
        "amount": amount,
        "phone_number": phone_number
    }
    mpesa = MpesaHandler()
    response = mpesa.make_stk_push(payload)
    print(response)
    return JsonResponse(response)

# query payment status

@csrf_exempt
def query_payment_status(request):
    if request.method == "POST":
        checkout_request_id = request.POST.get("checkout_request_id")
        mpesa = MpesaHandler()
        response = mpesa.query_transaction_status(checkout_request_id)
        print(response)
        return JsonResponse(response)
    else:
        return JsonResponse({"message": "method not allowed"}) 

# callback url
@csrf_exempt
def c2b_callback(request):
    if request.method == "POST":
        data = request.body
        try:
            # deserialize data
            data = json.loads(data)
            # write response to file
            with open("c2b_response.json", "a") as f:
                f.write(json.dumps(data))  # write the serialized JSON string directly
            # return data as jsonresponse
            return JsonResponse({"message": "success", "data": data})
        except Exception as e:
            print(str(e))
            return JsonResponse({"message": "error", "data": str(e)})
    else:
        return JsonResponse({"message": "method not allowed"})

@csrf_exempt
def register_c2b_urls(request):
    mpesa = MpesaHandler()
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v2/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": mpesa.shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": config("confirmation_url"),
               "ValidationURL": config("validation_url")}
    response = requests.post(api_url, json=options, headers=headers)
    return JsonResponse({"message": "success", "data": response.text})

# validation url
@csrf_exempt
def validation_url(request):
    data = request.body
    try:
        # deserialize data
        data = json.loads(data)
        # write response to file
        with open("c2b_validation.json", "a") as f:
            f.write(json.dumps(data))  # write the serialized JSON string directly
        # return data as jsonresponse
        context = {"ResultCode": 0, "ResultDesc": "Accepted"}
        return JsonResponse(dict(context))
    except Exception as e:
        print(str(e))
        return JsonResponse({"message": "error", "data": str(e)})

# confirmation url
@csrf_exempt
def confirmation_url(request):
    mpesa_body = request.body.decode("utf-8")
    mpesa_payment = json.loads(mpesa_body)
    print(mpesa_payment)

    with open("c2b_confirmation.json", "a") as f:
        f.write(json.dumps(mpesa_payment))

    context = {"ResultCode": 0, "ResultDesc": "Accepted"}

    return JsonResponse(dict(dict(context)))
