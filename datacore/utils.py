from oauth2client import client
import urllib
import requests
import jwt
import os

def get_id_token_with_code_method_1(code):
    
    credentials = client.credentials_from_clientsecrets_and_code(
        'client_secret.json',
        ['email', 'profile'],
        code
    )
    print(credentials.id_token)
    return credentials.id_token

def get_id_token_with_code_method_2(code):
    token_endpoint = "https://oauth2.googleapis.com/token"
    payload = {
        'code': code,
        'client_id': os.environ.get('SOCIAL_AUTH_GOOGLE_CLIENT_ID'),
        'client_secret': os.environ.get('SOCIAL_AUTH_GOOGLE_SECRET'),
        'grant_type': 'authorization_code',
        'redirect_uri': "postmessage",
    }
    body = urllib.parse.urlencode(payload)
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.post(token_endpoint, data=body, headers=headers)
    if response.ok:
        id_token = response.json().get('id_token', None)
        if id_token:
            return jwt.decode(id_token, options={"verify_signature": False})
    return None