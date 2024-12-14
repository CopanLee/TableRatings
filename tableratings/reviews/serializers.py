from rest_framework import serializers
from restaurant.models import Restaurant
from users.models import Users
from .models import Reviews
from datetime import date

class ReviewsSerializer(serializers.ModelSerializer):
    restaurant = serializers.CharField(source='restaurant.name', read_only=True)
    reviewer = serializers.CharField(source='reviewer.name', read_only=True)

    class Meta:
        model = Reviews
        fields = ['rating', 'review', 'date', 'restaurant', 'reviewer']


class GetReviewsSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField(default=None, source='restaurant.id')
    reviewer_id = serializers.IntegerField(default=None, source='reviewer.id')

class PostReviewsSerializer(serializers.Serializer):
    # use current date as default
    date = serializers.DateField(default=date.today)
    rating = serializers.IntegerField(min_value=0, max_value=5)
    review = serializers.CharField()
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    # restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    # reviewer = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

class PatchReviewsSerializer(serializers.Serializer):
    rating = serializers.IntegerField()
    review = serializers.CharField()

class DeleteReviewsSerializer(serializers.Serializer):
    # check if the reviewer is the same as the current user
    reviewer = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())


