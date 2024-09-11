from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.template.loader import get_template


def home(request):
    print("TEST - Homepage!")

    return render(request, template_name='home.html')

