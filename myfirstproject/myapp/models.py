from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator


class Place(models.Model):
    place_name = models.CharField(max_length=100, primary_key=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    category_choices = [
        ('Italian', 'Italian'),
        ('Chinese', 'Chinese'),
        ('Mexican', 'Mexican'),
        ('Gril', 'Gril'),
        ('Meat', 'Meat'),
        ('Seafood', 'Seafood'),
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan'),
        ('Fast_food', 'Fast Food'),
        ('Dessert', 'Dessert'),
        ('Cafe', 'Cafe'),
        ('Bar', 'Bar'),
        ('Pub', 'Pub'),
        ('Brewery', 'Brewery'),
        ('Steakhouse', 'Steakhouse'),
        ('Sushi', 'Sushi'),
        ('Food_truck', 'Food Truck'),
        ('Bakery', 'Bakery'),
        ('Deli', 'Deli'),
        ('Juice_bar', 'Juice Bar'),
        ('Asian', 'Asian'),
        ('Vietnamese','Vietnamese'),
        ('Morrocan','Morrocan'),
    ]
    category = models.CharField(max_length=100, choices=category_choices)
    is_cosher = models.BooleanField(default=False)
    has_vegan_option = models.BooleanField(default=False)
    recommended_dishes = models.TextField(blank=True)
    image = models.ImageField(upload_to='place_images/', default='')
    link = models.URLField(max_length=200, blank=True, null=True)
    rate = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]) 
    def __str__(self):
        return self.place_name


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

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class FoodSupplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    supplier_email = models.EmailField(unique=True)
    supplier_password = models.CharField(max_length=128,
                                          validators=[RegexValidator('^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=!]).{8,}$')])

    def __str__(self):
        return self.name
