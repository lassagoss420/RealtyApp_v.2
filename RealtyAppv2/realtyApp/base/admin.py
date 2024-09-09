from django.contrib import admin
from .models import Client, Listing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_no', 'category')


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    sortable_by = ('client',)
    list_filter = ('category', 'client')
    list_display = ('title', 'category', 'client')

