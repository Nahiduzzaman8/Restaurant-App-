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


from django.contrib.auth.models import User
def decode_jwt(request):
    try:
        token = request.COOKIES.get('token')
        payload = jwt.decode(token, Secret, algorithms= "HS256")
        userid = payload.get('userid')
        user = User.objects.get(id=userid)
        return user
    
    except jwt.ExpiredSignatureError as expired:
        return None
    
    except jwt.DecodeError as decodeerror:
        return None


# token = create_jwt(78)
# print((token))
