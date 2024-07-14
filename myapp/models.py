from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, password, **extra_fields)

    
class User (AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, primary_key=True)
    full_name = models.CharField(max_length=150)
    is_business_owner = models.BooleanField(default=False)  
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='places', null=True, blank=True) 
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    category_choices = [
        ('Israeli', 'Israeli'), ('Italian', 'Italian'), ('Chinese', 'Chinese'), ('Mexican', 'Mexican'), ('Grill', 'Grill'),
        ('Meat', 'Meat'), ('Seafood', 'Seafood'), ('Vegetarian', 'Vegetarian'), ('Vegan', 'Vegan'), ('Fast_food', 'Fast Food'),
        ('Dessert', 'Dessert'), ('Cafe', 'Cafe'), ('Bar', 'Bar'), ('Pub', 'Pub'), ('Brewery', 'Brewery'),
        ('Steakhouse', 'Steakhouse'), ('Sushi', 'Sushi'), ('Food_truck', 'Food Truck'), ('Bakery', 'Bakery'),
        ('Deli', 'Deli'), ('Juice_bar', 'Juice Bar'), ('Asian', 'Asian'), ('Vietnamese','Vietnamese'), ('Morrocan','Morrocan'),
    ]
    food_category = models.CharField(max_length=100, choices=category_choices, default='Israeli')
    is_kosher = models.BooleanField(default=False)
    has_vegan_option = models.BooleanField(default=False)
    recommended_dishes = models.TextField(blank=True)
    image = models.ImageField(upload_to='place_images/', default='',blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.place_name


