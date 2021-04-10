import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

class MpesaC2BCredential:
    consumer_key = 'bs84aD7VaJLrZosruylv9dAGi1dYnuJy'
    consumer_secret = 'UcgJr2x3xwlHg3GK'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

class MpesaAccessToken:
    r=requests.get(MpesaC2BCredential.api_URL,auth=HTTPBasicAuth(
        MpesaC2BCredential.consumer_key,
        MpesaC2BCredential.consumer_secret
    ))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    
class LipaNaMpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    business_short_code = "174379"
    test_c2b_shortcode = "603021"
    pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    
    data_to_encode = business_short_code + pass_key + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')