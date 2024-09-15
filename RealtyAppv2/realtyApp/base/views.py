from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.template.loader import get_template
from .models import Coordinates, Listing
import folium


def home(request):
    # rendering and creating the homepage with the map
    print("TEST - Homepage!")

    m = folium.Map(location=[19, -12], zoom_start=2) #creating the map object, need to automate passing the coords
    m = m._repr_html_() #html representation for the map
    context = {
        'm': m,
    }
    return render(request, template_name='home.html', context=context)


