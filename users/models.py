#Byimaan

from django.db import models
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager, User
import logging


def handle_user_image(instance,filename):
        
    try:
        return 'images/user-{0}/user_img/filename-{1}'.format(instance.id,filename)
    except Exception as Er:
        logging.exception("Error while handling the media file for the %s - %s" % (instance.email,Er))
        return 
    
# Create your models here.    

class CustomAccountManager(BaseUserManager):

    def create_superuser(self,email,user_name,password,**other_fields):

        other_fields.setdefault('is_staff',True)

        other_fields.setdefault('is_superuser', True)

        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff = True.'
            )
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser = True. '
            )
        print("A super user has been created (testing) -> ",other_fields['is_superuser'])
        return self.create_user(email,user_name,password,**other_fields)
    
    def create_user(self,email,user_name,password=None,**other_fields):

        other_fields['is_active'] = True

        if not email:
            raise ValueError(
                _('You must provide an email address')
                )
        
        email = self.normalize_email(email)
        
        user = self.model(email=email, user_name=user_name,**other_fields)

        user.set_password(password)

        user.save(using=self.db)

        return user


class NewUser(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(_('email address'),unique=True)

    user_name = models.CharField(max_length=150)

    first_name = models.CharField(max_length=150,blank=True)

    last_name = models.CharField(max_length=150,blank=True)

    start_date = models.DateTimeField(default=timezone.now)

    about = models.TextField(_('about'),max_length=300,blank=True)

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    is_superuser = models.BooleanField(default=False)

    user_image = models.ImageField(blank=True,null=True,upload_to=handle_user_image)

    objects = CustomAccountManager()


    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="customuser_set",  
        related_query_name="user",
        verbose_name=_('groups')
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",  
        related_query_name="user",
        verbose_name=_('user permissions')
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['user_name','first_name']

    def __str__(self):
        return self.user_name
    
