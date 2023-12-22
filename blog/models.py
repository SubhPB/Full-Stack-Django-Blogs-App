# from collections.abc import Iterable
from django.db import models
# from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.utils import timezone
from users.models import NewUser
import logging
from django.utils.text import slugify

def organize_media_file(instance,filename):
    try:
       return 'images/user-{0}/post-{1}/filename-{2}'.format(instance.author.id,instance.id,filename)
    except Exception as Er:
        logging.exception("Error while handling the media file for the post - %s",Er)
        return 

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Post(models.Model):

    # we want to display the data which is published and not in draft state
    class PostObjects(models.Manager):
        def get_queryset(self) -> QuerySet:
            return super().get_queryset().filter(status='published')


    options = [
        ('draft','Draft'),
        ('published','Published')
    ]

    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='categories') 

    title = models.CharField(max_length=250)

    excerpt = models.TextField(null=True,blank=True)

    content = models.TextField()

    slug = models.SlugField(max_length=250,unique_for_date='published',null=True,blank=True)

    published = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(NewUser,on_delete=models.CASCADE,related_name='blog_posts')   

    status = models.CharField(max_length=10, choices=options, default='published')

    objects = models.Manager()

    postobjects = PostObjects()

    image = models.ImageField(blank=True,null=True,upload_to=organize_media_file)

    image_url = models.CharField(max_length=500,null=True,blank=True,default="https://images.pexels.com/photos/171945/pexels-photo-171945.jpeg?auto=compress&cs=tinysrgb&w=400")

    class Meta:
        ordering = ('-published',)

    def save(self, *args,**kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super(Post,self).save(*args,**kwargs)    