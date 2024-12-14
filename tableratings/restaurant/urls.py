from django.urls import path
from .views import RestaurantListAPI, RestaurantDetailAPI

urlpatterns = [
    path('restaurants/', RestaurantListAPI.as_view(), name='restaurant-list'),
    path('restaurants/<int:id>/', RestaurantDetailAPI.as_view(), name='restaurant-detail'),
]