# CareApp/credentials.py
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

class MpesaC2bCredential:
    consumer_key = 'zrboAgmNWKFLSG0NTxUVl3cwCesUA4o9GGvmg3FIJU24PfJA'
    consumer_secret = 'TKoCGAUP3wBwb7L9KFktZD753TE9QcxtZmzLbNcYMD0pqVuwQrJi7VNHXm0KS2gd'
    BUSINESS_SHORT_CODE = "174379"
    PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

def get_mpesa_access_token():
    try:
        r = requests.get(MpesaC2bCredential.api_URL,
                         auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret),
                         timeout=10)
        r.raise_for_status()
        token_data = r.json()
        return token_data.get("access_token")
    except Exception as e:
        print("Failed to get token:", str(e))
        return None

def generate_stk_password():
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    business_short_code = "174379"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    data_to_encode = business_short_code + passkey + lipa_time
    password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
    return business_short_code, password, lipa_time