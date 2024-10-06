from django.db import models
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}' if self.user.first_name and self.user.last_name else self.user.username


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('buy', 'Buy'),
        ('rent', 'Rent'),
        ('sell', 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    str_address = models.CharField(max_length=255)
    str_number = models.CharField(max_length=10)
    description = models.TextField()

    def convert_to_coord(self):
        geolocator = Nominatim(user_agent="realty_app")
        full_address = f'{self.city}, {self.str_number}, {self.str_address}'
        coordinates = geolocator.geocode(full_address)

        if coordinates:
            latitude, longitude = coordinates.latitude, coordinates.longitude

            if hasattr(self, 'coordinates'):
                self.coordinates.latitude = latitude
                self.coordinates.longitude = longitude
                self.coordinates.save()
            else:
                Coordinates.objects.create(
                    listing=self,
                    latitude=latitude,
                    longitude=longitude
                )
            return True
        else:
            return False

    def save(self, *args, **kwargs):  # saves the listing instance
        super().save(*args, **kwargs)
        self.convert_to_coord()  # save coordinates upon saving a listing
        print('coords saved')  # test output

    def __str__(self):
        return self.title


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='listing/images/')


class Coordinates(models.Model):
    class Meta:
        db_table = 'coordinates'

    listing = models.OneToOneField(Listing, on_delete=models.CASCADE,
                                related_name='coordinates', null=True)  # one to one rel with listings model, one set of coords linked to one full address
    latitude = models.FloatField(null=True, blank=True)  # coords sunt float
    longitude = models.FloatField(null=True, blank=True)
