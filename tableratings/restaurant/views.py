from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Restaurant
from .serializers import GetRestaurantSerializer, PostRestaurantSerializer, RestaurantSerializer


class RestaurantListAPI(APIView):

    @swagger_auto_schema(
        query_serializer=GetRestaurantSerializer,
        responses={200: RestaurantSerializer(many=True)},
        security=[{'SessionAuth': []}]
    )
    def get(self, request):
        """
        Return a list of all restaurants
        """
        serializer = GetRestaurantSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = Restaurant.objects
        name = serializer.validated_data['name']
        rating = serializer.validated_data['rating']
        sort = serializer.validated_data['sort']
        sort_order = serializer.validated_data['sort_order']
        if name:
            queryset = queryset.filter(name=name)
        if rating:
            queryset = queryset.filter(rating__gte=rating)
        if sort:
            if sort_order == 'desc':
                sort = f'-{sort}'
            queryset = queryset.all().order_by(sort)
        serializer = RestaurantSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PostRestaurantSerializer,
        responses={201: RestaurantSerializer},
        security=[{'SessionAuth': []}]
    )
    def post(self, request):
        """
        Create a new restaurant
        """
        serializer = PostRestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RestaurantDetailAPI(APIView):
    @swagger_auto_schema(
        responses={200: RestaurantSerializer},
        security=[{'SessionAuth': []}]
    )
    def get(self, request, id):
        """
        Retrieve a restaurant by ID
        """
        try:
            restaurant = Restaurant.objects.get(pk=id)
        except Restaurant.DoesNotExist:
            return Response({'msg': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PostRestaurantSerializer,
        responses={200: RestaurantSerializer},
        security=[{'SessionAuth': []}]
    )
    def patch(self, request, id):
        """
        Update a restaurant by ID
        """
        try:
            restaurant = Restaurant.objects.get(pk=id)
        except Restaurant.DoesNotExist:
            return Response({'msg': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
