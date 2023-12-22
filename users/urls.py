from django.urls import path
from .views import CreateUserApiView, BlackListTokenView, UserDetails, UserAuthPatch, UserPatch

urlpatterns = [

    path('register/',CreateUserApiView.as_view(),name='create_user'),

    path('logout/blacklist/',BlackListTokenView.as_view(),name='blacklist'),

    path('data/',UserDetails.as_view(),name='user_data'),

    path('change/password/',UserAuthPatch.as_view(),name='user_change_password'),

    path('update/',UserPatch.as_view(),name='user_data_update')

]