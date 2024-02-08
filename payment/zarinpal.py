import requests
import json
from django.conf import settings


def send_request(amount, description=None, phone=None):
    # Default values if description and phone are not provided
    if not description:
        description = "Payment Description"  # Replace with a default description
    if not phone:
        phone = ''  # Leave empty or set a default phone number

    data = {
        "MerchantID": settings.ZARINPAL_MERCHANT_ID,
        "Amount": amount,
        "Description": description,
        "Phone": phone,
        "CallbackURL": settings.ZARINPAL_CALLBACK_URL,
    }
    headers = {'content-type': 'application/json'}

    try:
        response = requests.post(settings.ZARINPAL_API_REQUEST, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data['Status'] == 100:
                return {
                    'status': True,
                    'url': f"{settings.ZARINPAL_API_STARTPAY}{response_data['Authority']}",
                    'authority': response_data['Authority']
                }
            else:
                return {'status': False, 'code': str(response_data['Status'])}
        return {'status': False, 'error': 'Unexpected response status'}
    except requests.exceptions.Timeout:
        return {'status': False, 'error': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'error': 'connection error'}



def verify(authority, amount):
    data = {
        "MerchantID": settings.ZARINPAL_MERCHANT_ID,
        "Amount": amount,
        "Authority": authority,
    }
    headers = {'content-type': 'application/json'}

    try:
        response = requests.post(settings.ZARINPAL_API_VERIFY, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data['Status'] == 100:
                return {'status': True, 'RefID': response_data['RefID']}
            else:
                return {'status': False, 'code': str(response_data['Status'])}
        return {'status': False, 'error': 'Unexpected response status'}
    except requests.exceptions.RequestException as e:
        return {'status': False, 'error': str(e)}

