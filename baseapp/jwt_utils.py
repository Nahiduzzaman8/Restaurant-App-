import jwt
import datetime
from django.http import JsonResponse
# from django.conf import settings
Secret = "this is a secret key"

def create_jwt(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, Secret, algorithm= "HS256")
    return(token)


from django.contrib.auth.models import User
def decode_jwt(token):
    try:
        payload = jwt.decode(token, Secret, algorithms= "HS256")
        return payload
    
    except jwt.ExpiredSignatureError as expired:
        return None
    
    except jwt.DecodeError as decodeerror:
        return None

