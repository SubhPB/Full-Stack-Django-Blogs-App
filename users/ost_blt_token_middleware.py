from django.http import HttpResponseForbidden,HttpResponseBadRequest
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
import json
import base64
from users.models import NewUser as User

# jti - 8cd256f5652a4e66a30f4c2d2c31e527


class OST_BLT_middleware:

    def __init__(self,get_response):
        self.get_response = get_response
        

    def __call__(self,request):
        # self.logger.info(f"Request path: {request.path}")

        if request.method == 'POST':
            print("---- OST MIDDLEWARE STARTS HERE ----")

            print(type(request))

            print('')

            try:
                print("content type = ", request.content_type)
                print('')
                print("content params = ",request.content_params)
                print('')
                print("encoding used = ", request.encoding)
                print('')
                print("posted request = ", request.POST)
                print('')
                print(" META data of headers = ", request.META)
                print('')
                print(" header information = ", request.headers)
            except:
                print("exception was called")    


            if isinstance(request,dict):
                for k,v in request.items():
                    print('')
                    print("| key : {0} , value: {1} |".format(k,v))
                    print('')

    
            print("---- OST MIDDLEWARE ENDS HERE ----")

        


        # if request.method == 'POST' and request.path == '/api/user/logout/blacklist/':
        #     print(" --------------- Byimaan ---------------- ")

        #     raw_data = request.body
        #     print('raw data = ', raw_data)

        #     raw_data_text = raw_data.decode('utf-8')

        #     org_body_token = json.loads(raw_data_text)['refresh_token']

        #     header, token_encode, signature = org_body_token.split('.')

        #     token64_decode = base64.urlsafe_b64decode(token_encode).decode('utf-8')

        #     user_id = json.loads(token64_decode)['user_id']

        #     user = User.objects.all().filter(id=int(user_id))

        #     if user:
        #         print(user[0].email + " just logged out from the system.")

        #     else:
        #         print('Some unexpected thing happened, may be result into a duplicate data or an error in the future')    
            
        #     print(" -------- Hussle and Motivate ------------")


        return self.get_response(request)