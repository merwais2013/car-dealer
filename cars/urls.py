from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_cars_by_query_params, name='cars'),
    path('search/',views.get_cars_by_searching, name='search'),
    path('multiple/',views.get_cars_by_multiple_serach, name='multiple-search'),
    path('contact/', views.contact, name='contact'),
    path('latest/',views.latest_cars, name='latest-cars'),
    path('inbox/', views.inbox, name='inbox'),
    path('send_message/<str:pk>/', views.send_message,name='message'),
    path('<str:pk>/', views.get_single_car, name='single-car'),
]