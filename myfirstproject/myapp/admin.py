from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FoodSupplier, Place

admin.site.register(User)
admin.site.register(FoodSupplier)
admin.site.register(Place)
