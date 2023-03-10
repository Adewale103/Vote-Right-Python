import os
import requests
import json
from dotenv import load_dotenv
import uuid
from .models import User

load_dotenv()

BVN_VALIDATION_ENDPOINT = 'https://api.flutterwave.com/v3/kyc/bvns/'
FLUTTERWAVE_API_KEY = os.getenv('FLUTTERWAVE_API_KEY')
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {FLUTTERWAVE_API_KEY}',
}


def validate_bvn(bvn):
    request_body = {
        'bvn': bvn,
    }
    response = requests.post(BVN_VALIDATION_ENDPOINT, headers=HEADERS, data=json.dumps(request_body))
    response.raise_for_status()
    response_data = response.json()
    return ValidateBVNResponse(
        status=response_data['status'],
        message=response_data['message'],
        data=response_data['data'],
    )


def generate_username(first_name, last_name):
    username = (first_name + str(uuid.uuid4())[:4] + last_name[:4]).lower()
    while User.objects.filter(username=username).exists():
        username = (first_name + str(uuid.uuid4())[:4] + last_name[:4]).lower()
    return username


class ValidateBVNResponse:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data
