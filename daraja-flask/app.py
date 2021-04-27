from flask import Flask, render_template, request
import requests
import json
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

from decouple import config

#daraja credentials
consumer_key = config('consumer_key')
consumer_secret = config('consumer_secret')
base_url = 'https://b0a82b93f246.ngrok.io'


@app.route('/')
def home():
    return 'Hello There..lets do this'

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=8080, debug=True)
    
    
#register url
@app.route('/c2b/register_urls')
def register_urls():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization":"Bearer %s" % create_access_token()}
    req_body = {
        "ShortCode": "603021",
        "ResponseType": "Completed",
        "ConfirmationURL": "https://b0a82b93f246.ngrok.io/c2b/confirm",
        "ValidationURL": "https://b0a82b93f246.ngrok.io/c2b/validate"}
    response_data = requests.post(mpesa_endpoint,json=req_body, headers=headers)
    return response_data.json()

@app.route('/c2b/confirm', methods=['POST'])
def confimation_url():
    data = request.get_json()
    file = open('confirm.json','a')
    file.write(json.dumps(data))
    file.close()
    
    return {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    
@app.route('/c2b/validate', methods=['POST'])
def validate():
    data = request.get_json()
    file = open('validate.json','a')
    file.write(json.dumps(data))
    file.close
    
    return {
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    
    
@app.route('/c2b/simulate')
def simulate_trans():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    access_token = create_access_token()
    headers = {"Authorization":"Bearer %s" % access_token}
    req_body = {
        "ShortCode":"603021",
        "CommandID":"CustomerPayBillOnline",
        "Amount":"500",
        "Msisdn":"254708374149",
        "BillRefNumber":"TestPay1" }
    simulate_response = requests.post(mpesa_endpoint, json = req_body, headers=headers)
    return simulate_response.json()

#access token view
@app.route('/get_access_token')
def get_access_token():
    data = create_access_token()
    return data

def create_access_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    data = (requests.get(mpesa_auth_url, auth = HTTPBasicAuth(consumer_key, consumer_secret))).json()
    return data['access_token']
    
    