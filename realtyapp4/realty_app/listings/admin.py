from django.contrib import admin
from .models import UserProfile
from .models import Listing

admin.site.register(UserProfile)
admin.site.register(Listing)