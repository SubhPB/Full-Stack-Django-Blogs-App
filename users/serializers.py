
from rest_framework import serializers  
from .models import NewUser  
from blogapi.serializers import PostSerializer
from blog.models import Post


class NewUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = NewUser
        fields = ('email','user_name','password','user_image')
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):

        password = validated_data.pop('password',None)

        if password is not None and len(password) >= 4:
            user = NewUser.objects.create_user(
                email=validated_data.get('email'),
                user_name=validated_data.get('user_name'),
                password=password,
                user_image= validated_data.pop('user_image',None)
            )

        else:
            raise ValueError(
                'Oops!, SomeThing went wrong.'
            ) 

        return user

    
class UserData(serializers.ModelSerializer):
    
    blogs = serializers.SerializerMethodField()

    class Meta:
        model = NewUser
        fields= ('id','email','user_name','first_name','user_image','blogs') 

    def get_blogs(self,obj):
        posts = Post.objects.filter(author=obj) 
        return PostSerializer(posts,many=True).data   
    
          

class ChangeUserPassword(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


    def validate(self, data):

        if len(data['new_password']) < 4:
            raise serializers.ValidationError(
                'Given password is too short'
            )

        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError(
                'Old password should be different from the new one.'
            )
        
        if not self.context['user'].check_password(data['old_password']):
            raise serializers.ValidationError(
                'The given password is not valid'
            )

        return data
        
class UserDataUpdate(serializers.ModelSerializer):

    class Meta:
        model = NewUser    
        fields = ('user_name','user_image')

    def validate_user_name(self,value):
        if len(value) < 4: 
            raise serializers.ValidationError(
                'Given user_name is too short'
            )
        return value

    def update(self,instance,validated_data):

        for attr,val in validated_data.items():

            setattr(instance,attr,val)  


        instance.save()

        return instance    
 