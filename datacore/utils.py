from oauth2client import client
import urllib
import requests
import jwt
import os
from django.core.mail import send_mail
from django.conf import settings
from .models import User



def enviar_email(asunto,id_user, mensaje):
    try:
        usuario = User.objects.get(id=id_user)
        destinatario = usuario.email
    except User.DoesNotExist:
        raise ValueError("Usuario no encontrado.")

    asunto = asunto
    destinatarios = [destinatario]

    send_mail(
        asunto,
        mensaje,
        None,
        destinatarios
    )




def get_id_token_with_code_method_1(code):
    credentials = client.credentials_from_clientsecrets_and_code(
        "client_secret.json", ["email", "profile"], code
    )
    print(credentials.id_token)
    return credentials.id_token


def get_id_token_with_code_method_2(code):
    token_endpoint = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID"),
        "client_secret": os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET"),
        "grant_type": "authorization_code",
        "redirect_uri": "postmessage",
    }
    body = urllib.parse.urlencode(payload)
    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.post(token_endpoint, data=body, headers=headers)
    if response.ok:
        id_token = response.json().get("id_token", None)
        if id_token:
            return jwt.decode(id_token, options={"verify_signature": False})
    return None
