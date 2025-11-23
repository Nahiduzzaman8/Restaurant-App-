import jwt
import datetime
# from django.conf import settings




Secret = "this is a secret key"

def create_jwt(userid):
    payload = {
        "userid":userid, 
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, Secret, algorithm="HS256")
    print(token)
create_jwt(67)
# print("nahid")
# print(datetime.datetime.now())
# print(timezone.now())
# from django.utils import timezone
# print(datetime.datetime.utcnow())