from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from .forms import UserLoginForm
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# todo
# add views to urls!!!!


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, message=f'Account created for {user.email}!')
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, template_name='client_app/register.html', context={'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, message='Invalid credentials.')

    else:
        form = UserLoginForm()

    return render(request, template_name='client_app/login.html', context={'form': form})


@login_required
def profile(request):
    client = request.user.profile
    listings = client.listings.all()
    return render(request, 'client_app/profile.html', {'client': client, 'listings':listings})


def logout_view(request):
    logout(request)
    return redirect('login')