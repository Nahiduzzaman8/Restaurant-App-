import jwt
import datetime
# from django.conf import settings
Secret = "this is a secret key"

def create_jwt(userid):
    payload = {
        "userid":userid, 
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15) # need to study about this
    }
    token = jwt.encode(payload, Secret, algorithm= "HS256")
    return(token)

def decode_jwt(token):
    try:
        payload = jwt.decode(token, Secret, algorithms= "HS256")
        return(payload)
    except jwt.ExpiredSignatureError as expired:
        return expired
    except jwt.DecodeError as decodeerror:
        return decodeerror


# token = create_jwt(78)
# print((token))
