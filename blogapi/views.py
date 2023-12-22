from rest_framework import generics, views,response, status, filters 
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from .api_custom_permissions import IsBlogOwner
from django.core.files.storage import default_storage

class PostList(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    # authentication_classes = [JWTAuthentication]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'category__name','author__user_name']

 
class PostDetail(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CreateBlog(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]


    def post(self,request):

        serializer = PostSerializer(data=request.data,context={'request':request})

        if serializer.is_valid():

            newpost = serializer.save()

            if newpost:
                return response.Response(
                    serializer.data
                    ,
                    status=status.HTTP_201_CREATED
                )       

        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)         
    
class PersonalBlogs(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsBlogOwner]
    parser_classes = [MultiPartParser,FormParser]

    def get(self,request,pk=None,size=None):
        
        if pk:
            try:
                blog = Post.objects.get(id=pk, author=request.user)

            except Post.DoesNotExist:
                return response.Response({
                    'error':'Blog Does not exists.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = PostSerializer(blog)

            return response.Response(
                serializer.data,
                status= status.HTTP_200_OK
            )
        
        blogs = Post.objects.filter(author=request.user)[:size] if size else Post.objects.filter(author=request.user) 
        serializer = PostSerializer(blogs,many=True)

        
        return response.Response(serializer.data,status=status.HTTP_200_OK)
            
    def patch(self,request,pk=None,size=None):

        if pk:
            try:
                blog = Post.objects.get(id=pk)  

                serializer = PostSerializer(blog,data=request.data,partial=True)

                if serializer.is_valid():

                    new_image = request.FILES.get('image',None)

                    if new_image:
                        if blog.image:
                            old_img_path = blog.image.path

                            if default_storage.exists(old_img_path):
                                default_storage.delete(old_img_path)

                    serializer.save()
                    return response.Response(
                        serializer.data,status=status.HTTP_200_OK
                    )
                
                else:
                    return response.Response(
                        serializer.errors,status=status.HTTP_400_BAD_REQUEST
                    )
            except Post.DoesNotExist:
                
                return response.Response(
                    {"error":'Blog does not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return response.Response({ 
            'error':'Blog Id is required for patch method.'
            }, status=status.HTTP_400_BAD_REQUEST
        )       
    
    def delete(self,request,pk=None):

        if pk:
            try:
                blog = Post.objects.get(id=pk)

                blog.delete();
                
                return response.Response({
                    'data': " Given blog was deleted"
                }, status=status.HTTP_200_OK)
            
            except Post.DoesNotExist:

                return response.Response({
                    'data': 'Given blog id does not exist'
                },status=status.HTTP_404_NOT_FOUND)
            
        return response.Response({
            'error': 'Blog id is required'
        },status=status.HTTP_400_BAD_REQUEST) 
     
#  posted request =  <QueryDict: {'title': ['something in title'],
#  'category.name': ['tech'], 'content': ['blah blah content'],
#  'excerpt': ['blah blah excerpt'], 'status': ['publish']}>


# posted request =  <QueryDict: {'title': ['Ocean Conservation: Protecting Our Marine Ecosystems'],
#  'category.name': ['Sea Life'],
#  'excerpt': ['Our oceans are in peril. Learn about the urgent need for ocean conservation and what we can do to help.'],
#  'content': ["The world's oceans are facing unprecedented threats due to pollution, overfishing, and climate change. 
# This article highlights the critical importance of ocean conservation, discussing the current state of marine ecosystems,
#  the impact of human activities, and the efforts being made to protect and restore marine biodiversity. It also provides 
# practical ways individuals and communities can contribute to ocean conservation, emphasizing the role everyone plays in
#  safeguarding these vital ecosystems for future generations."], 'status': ['published']}>

