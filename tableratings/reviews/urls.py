from django.urls import path
from .views import ReviewsAPI, ReviewsDetailAPI

urlpatterns = [
    path('reviews', ReviewsAPI.as_view(), name='reviews-list'),
    path('reviews/<int:id>', ReviewsDetailAPI.as_view(), name='reviews-detail'),
]