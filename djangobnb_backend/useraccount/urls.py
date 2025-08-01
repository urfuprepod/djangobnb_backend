from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .api import landlord_detail, reservations_list

urlpatterns = [
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('token/refresh/', get_refresh_view().as_view(), name='rest_refresh'),
    path('logout/', LogoutView.as_view(), name='rest_logout'), 
    path('<uuid:pk>/', landlord_detail, name='api_landlord_detail'),
    path('myreservations', reservations_list, name='api_reservations_list')
]
