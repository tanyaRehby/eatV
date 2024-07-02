from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Place


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'autofocus': True}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'is_business_owner']

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['place_name', 'city', 'address', 'longitude', 'latitude', 'food_category', 'is_kosher', 'has_vegan_option']
