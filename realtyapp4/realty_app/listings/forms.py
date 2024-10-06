from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Listing, ListingImage


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone_number', 'street_address', 'profile_picture', 'bio']


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'title', 'price', 'city', 'str_address', 'str_number', 'description']


class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image']


class MultiImageForm(forms.Form):
    images = forms.FileField(required=False)

