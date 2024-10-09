import folium
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserRegisterForm, UserProfileForm, ListingForm, MultiImageForm, ListingImage
from .models import Listing


def home(request):
    listings = Listing.objects.all().select_related('coordinates')

    category_filter = request.GET.get('category')
    if category_filter:
        listings = listings.filter(category=category_filter)

    city_filter = request.GET.get('city')
    if city_filter:
        listings = listings.filter(city__iexact=city_filter)

    map_center = [45.9852129, 24.6859225]
    folium_map = folium.Map(location=map_center, zoom_start=6 )

    for listing in listings:
        if listing.coordinates and listing.coordinates.latitude and listing.coordinates.longitude:
            popup_html = f"""
            <b>{listing.title}</b><br>
            Price: ${listing.price}<br>
            Address: {listing.str_address}, {listing.str_number}, {listing.city}<br>
            <a href="{reverse('listing_detail', args=[listing.id])}">View Details</a>
            """
            folium.Marker(
                [listing.coordinates.latitude, listing.coordinates.longitude],
                popup=popup_html,
                tooltip=listing.title
            ).add_to(folium_map)

    map_html = folium_map._repr_html_()

    return render(request, 'listings/home.html', {
        'listings': listings,
        'map_html': map_html
    })


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'listings/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'listings/login.html')


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'listings/profile.html', {'profile_form': profile_form})


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        image_form = MultiImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()

            images = request.FILES.getlist('images')
            for img in images:
                ListingImage.objects.create(listing=listing, image=img)

            return redirect('home')

    else:
        form = ListingForm()
        image_form = MultiImageForm()

    return render(request, 'listings/create_listing.html',
                {'form': form, 'image_form': image_form})


@login_required
def user_listings(request):
    user_listings = Listing.objects.filter(user=request.user)
    return render(request, 'listings/user_listings.html', {'listings': user_listings})


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'listings/listing_detail.html', {'listing': listing})


@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        image_form = MultiImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            form.save()

            images = request.FILES.getlist('images')
            for image in images:
                ListingImage.objects.create(listing=listing, image=image)

            return redirect('listing_detail', listing_id=listing.id)
    else:
        form = ListingForm(instance=listing)
        image_form = MultiImageForm()

    return render(request, 'listings/edit_listing.html',
                {'form': form, 'image_form': image_form, 'listing': listing})


@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if listing.user == request.user:
        listing.delete()
        return redirect('home')

    return redirect('listing_detail', listing_id=listing_id)