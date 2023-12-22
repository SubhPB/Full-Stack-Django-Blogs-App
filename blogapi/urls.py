from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView  
)
from .views import PostList,PostDetail,CreateBlog, PersonalBlogs
from users.views import AccessTokenInquery, RefreshTokenInquery
 
app_name = 'blogapi'

urlpatterns = [
    # this url gives the detail of a single specific post
    path('<int:pk>',PostDetail.as_view(),name="detailcreate"),

    #  this url gives the list of posts.
    path('',PostList.as_view(),name='listcreate'),

    # api endpoint for personal blogs
    path('personal/blogs/<int:size>/',PersonalBlogs.as_view(),name='personalblogs'),
    path('personal/<int:pk>/blogs/',PersonalBlogs.as_view(),name='personalblogs'),
    path('personal/blogs/',PersonalBlogs.as_view(),name='personalblogs'),
    
    # Access-token 
    path('token/',TokenObtainPairView.as_view(),name='token_obtain'),

    # additional api endpoint for checking the existing access token
    path('access_token/info/',AccessTokenInquery.as_view(),name='access_token_check'),

    # api endpoint for the inquery of refresh token
    path('refresh_token/info/',RefreshTokenInquery.as_view(),name='refresh_token_check'),

    # Refresh-token  
    path('token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),

    # registering user through API 
    path('user/',include('users.urls'),name='users'),

    # for creasting the blog
    path('blog/create/',CreateBlog.as_view(),name='createblog'),
 
]