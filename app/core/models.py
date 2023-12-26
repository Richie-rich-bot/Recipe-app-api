from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,password = None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
                raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email = email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_superuser(self,email, password= None):
         """Create and return a new superuser"""
         user = self.create_user(email, password)
         user.is_staff = True
         user.is_superuser = True
         user.save(using=self._db)
         return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length= 255, unique = True)
    name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

class Recipe(models.Model):
    """Recipe objects"""
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
              on_delete = models.CASCADE,
    )
    title = models.CharField(max_length = 255)
    description = models.TextField(blank = True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredients')

    def __str__(self):
        return self.title 
    
class Tag(models.Model):
    name = models.CharField(max_length= 255)
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
              on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.name
    

class Ingredients(models.Model):
    """Ingredients for reccipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    
    def __str__(self):
        return self.name