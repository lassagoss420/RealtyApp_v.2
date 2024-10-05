from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.template.loader import get_template
from .models import Coordinates, Listing
import folium


def home(request):  # need to implement map, search, add, register/login and
    # rendering and creating the homepage with the map
    print("TEST - Homepage!")

    m = folium.Map(location=[45.9852129, 24.6859225], zoom_start=7)  # creating the map object, need to automate passing the coords

    coord_list = Coordinates.objects.all()

    for coord in coord_list:
        if coord.latitude is not None and coord.longitude is not None:
            folium.Marker(
                location=[coord.latitude, coord.longitude],
                tooltip=f'{coord.listing}',
                popup=f'{coord.listing}',
            ).add_to(m)

    m = m._repr_html_()  # html representation for the map

    context = {
        'm': m,
    }
    return render(request, template_name='home.html', context=context)


