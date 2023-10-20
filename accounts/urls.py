from django.urls import path
from .views import MyTokenObtainPairView, register_user, update_profile, change_password

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('register/', register_user, name='register'),
    path('update/', update_profile, name='update'),
    path("change_password/", change_password, name='change-password'),
]