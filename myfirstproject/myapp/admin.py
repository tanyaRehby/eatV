from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Journey, Register_to_journey

admin.site.register(Users)
admin.site.register(Journey)
admin.site.register(Register_to_journey)
