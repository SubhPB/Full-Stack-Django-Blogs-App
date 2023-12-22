from typing import Any
from django.http import HttpResponseForbidden,HttpResponseBadRequest
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
import json
import base64
from users.models import NewUser as User

BASE_URL = '/api/'

class Custom_auth_routing_middleware:

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.method  == 'POST' and request.path == BASE_URL + 'token/':

           print("-- token route testing --")

           print(request.body)

           print("-- end of token route testing --")

        return self.get_response(request)   