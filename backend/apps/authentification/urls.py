from django.urls import path
from .views import (
    RegisterView, login_view, logout_view, 
    UserProfileView, user_stats_view
)

app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('stats/', user_stats_view, name='user-stats'),
]