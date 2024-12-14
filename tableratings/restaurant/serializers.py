from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
    

class GetRestaurantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(default=None)
    rating = serializers.IntegerField(default=None, min_value=0, max_value=5)
    sort = serializers.CharField(default='id')
    sort_order = serializers.CharField(default='asc')


    class Meta:
        model = Restaurant
        fields = ['name', 'rating', 'sort', 'sort_order']
    

class PostRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone', 'website']
