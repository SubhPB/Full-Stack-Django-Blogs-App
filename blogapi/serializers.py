# Byimaan


from rest_framework import serializers
from blog.models import Post, Category
from users.models import NewUser as User

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
 
    # author = NewUserSerializer()
    category = CategorySerializer()

    author = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(queryset=Category.objects.all(),slug_field='name')

    class Meta:
        model = Post
        fields = ('id','title','category','author','excerpt','image_url','content','status','image')
        
    def create(self,validated_data):
        title = validated_data.pop('title',None)
        category_data = validated_data.pop('category',{'name':'Unknown'})
        content = validated_data.pop('content',None)
        excerpt = validated_data.pop('excerpt','not given')
        status = validated_data.pop('status','published')
        author = self.context['request'].user
        image = validated_data.pop('image',None)
        image_url = validated_data.pop('image_url',None)

        category_name = f"({category_data['name']})".capitalize()
        category_inst = Category.objects.filter(name=category_name).first()

        if category_inst:
            category = category_inst
        else:
            category, _ = Category.objects.get_or_create(**category_data)

        try:
            
            post = Post.objects.create(
                title = title,
                content= content,
                status = status,
                author = author,
                category = category,
                excerpt= excerpt,
                image= image,
                image_url= image_url,
            )

            return post
        
        except Exception as e:
            raise e
        
    def update(self,instance,validated_data):
        category_data = validated_data.pop('category',None)

        if category_data:
            category_name = category_data.get('name','Unknown') 
            category, created = Category.objects.get_or_create(name= category_name)
            instance.category = category  

        for attr,val in validated_data.items():
            setattr(instance,attr,val)

        instance.save()

        return instance    
    
    def get_author(self,obj):
        return obj.author.user_name
