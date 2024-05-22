from django.db import models
import json

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import BaseUserManager
 


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # Ensure email is normalized
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class Users(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"ID: {self.pk}, Email: {self.email}, Name: {self.first_name} {self.last_name}"




class Journey(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    journey_name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveBigIntegerField()
    steps = models.PositiveIntegerField()
    category = models.TextField()
    image_url = models.URLField(default='')
    def set_category(self, category_list):
        self.category = json.dumps(category_list)

    def get_category(self):
        try:
            return json.loads(self.category)
        except json.JSONDecodeError:
            return []

    def __str__(self):
        return f"ID: {self.id}, Name: {self.journey_name} (Category: {', '.join(self.get_category())})"
   


class Register_to_journey(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.journey.journey_name}"
