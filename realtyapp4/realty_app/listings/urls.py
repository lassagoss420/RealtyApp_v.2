from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from realty_app import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('user_listings/', views.user_listings, name='user_listings'),
    path('listing/create/', views.create_listing, name='create_listing'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:listing_id>/edit/', views.edit_listing, name='edit_listing'),
    path('listing/<int:listing_id>/delete/', views.delete_listing, name='delete_listing'),
]




#  template_name='listings/logout.html'

