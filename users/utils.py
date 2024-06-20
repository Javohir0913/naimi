
# import requests
# from django.conf import settings
#
#
# def get_eskiz_token():
#     url = f"{settings.ESKIZ_API_URL}/auth/login"
#     payload = {
#         'email': settings.ESKIZ_EMAIL,
#         'password': settings.ESKIZ_PASSWORD
#     }
#     response = requests.post(url, data=payload)
#     response.raise_for_status()
#     return response.json()['data']['token']


def send_sms(phone, message):
    token = get_eskiz_token()
    url = f"{settings.ESKIZ_API_URL}/message/sms/send"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'mobile_phone': phone,
        'message': message,
        'from': '4546'
    }
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()
