from django.db import models
from geopy.geocoders import Nominatim
# from client_app.models import Client


# class Client(models.Model):
#     class Meta:
#         db_table = 'clients'
#         get_latest_by = "created_at"
#
#     CATEGORY = (
#         ('Client', 'Client'),
#         ('Agent', 'Agent'),
#     )
#
#     category = models.CharField(max_length=255, null=True, choices=CATEGORY)
#     name = models.CharField(max_length=255, null=True, blank=True)
#     email = models.EmailField(max_length=126, null=True, blank=True)
#     phone_no = models.CharField(max_length=10, null=True, blank=True, verbose_name='Phone No.')
#     str_addr = models.CharField(max_length=255, null=True, blank=True, verbose_name='Street Address')
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name


class Listing(models.Model):
    class Meta:
        db_table = 'listings'
        get_latest_by = "order_date"

    CATEGORY = (
        ('Buy', 'Buy'),  #maybe delete this? :) faulty logic or could it be a default homepage view?
        ('Sell', 'Sell'),
        ('Rent', 'Rent'),
        )

    category = models.CharField(max_length=255, null=True, choices=CATEGORY)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='City')
    str_addr = models.CharField(max_length=255, null=True, blank=True, verbose_name='Street Name')
    str_no = models.CharField(max_length=10, null=True, blank=True, verbose_name='Street Number')
    description = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey('client_app.Client', on_delete=models.CASCADE, related_name='listings')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_client_name(self):
        return self.client.name

    def convert_to_coord(self):
        geolocator = Nominatim(user_agent="realty_app")
        full_address = f'{self.city}, {self.str_no}, {self.str_addr}'  ##full address variable composition OSM uses city-str_no-str_name order, HAS to be dict|str not a tuple
        coordinates = geolocator.geocode(full_address)

        if coordinates:  # checks if coordinates already exist for this listing
            latitude, longitude = coordinates.latitude, coordinates.longitude

            if hasattr(self, 'coordinates'):  # updates existing coordinates

                self.coordinates.latitude = latitude
                self.coordinates.longitude = longitude
                self.coordinates.save()
            else:
                Coordinates.objects.create(  # creates new coordinates record
                    listing=self,
                    latitude=latitude,
                    longitude=longitude
                )
            return True
        else:
            return False

    def save(self, *args, **kwargs):  # saves the listing instance overrides base save method
        super().save(*args, **kwargs)
        self.convert_to_coord()  # added func to save button when saving an existing or new listing it runs above method and saves coords, lat and long, in coordinates db_table
        print('coords saved')  # test


class Coordinates(models.Model):
    class Meta:
        db_table = 'coordinates'

    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='coordinates', null=True)  #one to one rel with listings model, one set of coords linked to one full address
    latitude = models.FloatField(null=True, blank=True)  #coords sunt float
    longitude = models.FloatField(null=True, blank=True)



