from django.shortcuts import render
from django.conf import settings
import requests
import json

ZP_API_REQUEST = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"

amount = 10000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = '09177157497'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/verify/'


from django.http import JsonResponse
import requests
import json

def send_request(request):
    ZP_API_REQUEST = "https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
    amount = 10000  # Set your amount
    description = "Your Description"  # Set your description
    phone = '09177157497'  # Optional
    CallbackURL = 'http://127.0.0.1:8080/verify/'  # Set your Callback URL

    data = {
        "MerchantID": "e63b2dea-4e84-11e7-b42a-000c295eb8fc",
        "Amount": amount,
        "Description": description,
        "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    headers = {'content-type': 'application/json'}

    try:
        response = requests.post(ZP_API_REQUEST, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data['Status'] == 100:
                return JsonResponse({'status': True, 'url': f"{ZP_API_STARTPAY}{response_data['Authority']}", 'authority': response_data['Authority']})
            else:
                return JsonResponse({'status': False, 'code': str(response_data['Status'])})
        return JsonResponse({'status': False, 'error': 'Unexpected response status'})
    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'error': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'error': 'connection error'})

def verify(authority):
    data = {
        "MerchantID": "e63b2dea-4e84-11e7-b42a-000c295eb8fc",
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response