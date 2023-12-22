# Author - Byimaan $ubhpreet 

from django.shortcuts import render
from .serializers import NewUserSerializer, UserData, ChangeUserPassword, UserDataUpdate
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from .CustomApiPermissions import IsHimself
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage

# Create your views here.


class CreateUserApiView(APIView):

    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser,FormParser]

    def post(self,request):
        serializer = NewUserSerializer(data=request.data)
        
        if serializer.is_valid():

            newuser = serializer.save()

            refresh = RefreshToken.for_user(newuser)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            if newuser:
                return Response({
                    "access": access_token,
                    "refresh": refresh_token
                },status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)    

# Only the owner of the account can access this endpoint to get every data about himself.
class UserDetails(APIView):
    permission_classes = [IsAuthenticated,IsHimself]
    authentication_classes = [JWTAuthentication]

    def get(self,request):

        serializer = UserData(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserAuthPatch(APIView):

    permission_classes = [IsAuthenticated,IsHimself]
    authentication_classes = [JWTAuthentication]


    def patch(self,request):

        serializer = ChangeUserPassword(data=request.data,context={'user':request.user})

        try:
            if serializer.is_valid():
                # we already checked the password of user in serializer
                user = request.user

                user.set_password(request.data['new_password'])

                user.save()

                return Response({
                    'data': 'Your password has been updated.',
                }, status=status.HTTP_200_OK)

            else:
                return Response(
                    serializer.errors,status=status.HTTP_400_BAD_REQUEST
                ) 
        except Exception as e:
            return Response({
                'error': "Root Error!. " + f'{e}'
            },status=status.HTTP_400_BAD_REQUEST)

class UserPatch(APIView):

    permission_classes = [IsAuthenticated,IsHimself]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser,FormParser]
                   
    def patch(self,request):
        user = request.user

        serializer = UserDataUpdate(user,data=request.data,partial=True)   

        if serializer.is_valid():

            # let's delete the old image if new image has been uploaded
            new_image = request.FILES.get('user_image',None)

            if new_image:
                if user.user_image:
                    old_image_path = user.user_image.path

                    if default_storage.exists(old_image_path):
                        default_storage.delete(old_image_path)

            serializer.save()

            return Response(
                serializer.data,status=status.HTTP_200_OK
            )       

        return Response(
            serializer.errors,status=status.HTTP_400_BAD_REQUEST
        ) 
    
class BlackListTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):

        try: 
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)

        except Exception as error:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AccessTokenInquery(APIView):

    permission_classes = [AllowAny]

    def post(self,request):

        access_token = request.data['access']

        if not access_token:
            return Response({
                "error": "Access token is required in the field."
            },status=status.HTTP_400_BAD_REQUEST)

        try: 
            UntypedToken(access_token)

            decoded_token = UntypedToken(access_token).payload

            response = {
                "is_valid": True,
                "expiry_date": decoded_token.get('exp')
            }

            return Response(response,status=status.HTTP_200_OK)

        except:
            print(f"Invalid token given by the {request.user}. exp-date-details {None}")
            return Response({ 
                    'data' : "Invalid token information. try again",
                  },
                status=status.HTTP_401_UNAUTHORIZED
            ) 


class RefreshTokenInquery(APIView):

    permission_classes = {AllowAny}

    def post(self,request):

        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({
                'error': " refresh field is required..."
            },status=status.HTTP_400_BAD_REQUEST)
        
        try:
            decoded_token = RefreshToken(refresh_token)

            return Response({
                'valid': True,
                'exp': decoded_token.access_token.get('exp')
            },status=status.HTTP_202_ACCEPTED)
        
        except Exception as e:

            return  Response({
                'valid': False,
                'error': str(e)
            },status=status.HTTP_400_BAD_REQUEST)  