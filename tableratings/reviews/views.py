from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import Reviews
from .serializers import ReviewsSerializer, GetReviewsSerializer, PostReviewsSerializer, PatchReviewsSerializer


class ReviewsAPI(APIView):
    @swagger_auto_schema(
        query_serializer=GetReviewsSerializer,
        responses={200: ReviewsSerializer(many=True)},
        security=[{'SessionAuth': []}]
    )
    def get(self, request):
        """
        Return a list of restaurant reviews or reviewer reviews
        """
        serializer = GetReviewsSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        restaurant_id = serializer.validated_data['restaurant']['id']
        reviewer_id = serializer.validated_data['reviewer']['id']
        if restaurant_id is None and reviewer_id is None:
            return Response({'message': 'Restaurant or reviewer is required'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Reviews.objects
        if restaurant_id is not None:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        if reviewer_id is not None:
            queryset = queryset.filter(reviewer_id=reviewer_id)
        queryset = queryset.all().order_by('id')
        serializer = ReviewsSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PostReviewsSerializer,
        responses={201: 'Rating successful'},
        security=[{'SessionAuth': []}]
    )
    def post(self, request):
        """
        Create a new review
        """
        serializer = PostReviewsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.validated_data['reviewer_id'] = request.user['id']
        Reviews.objects.create(**serializer.validated_data)
        restaurant_obj = serializer.validated_data['restaurant']
        Reviews.update_average_rating(restaurant_obj.id)
        return Response({}, status=status.HTTP_201_CREATED)


class ReviewsDetailAPI(APIView):
    @swagger_auto_schema(
        request_body=PatchReviewsSerializer,
        responses={200: 'Review updated'},
        security=[{'SessionAuth': []}]
    )
    def patch(self, request, id):
        """
        Update a review
        """
        try:
            serializer = PatchReviewsSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            review = Reviews.objects.get(pk=id)
            if review.reviewer.id != request.user['id']:
                return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            review.rating = serializer.validated_data['rating']
            review.review = serializer.validated_data['review']
            review.save()
            Reviews.update_average_rating(review.restaurant.id)
        except Reviews.DoesNotExist:
            return Response({'message': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Review updated'})

    @swagger_auto_schema(
        responses={204: 'Review delete'},
        security=[{'SessionAuth': []}]
    )
    def delete(self, request, id):
        """
        Delete a review
        """
        try:
            review = Reviews.objects.get(pk=id)
            if review.reviewer.id != request.user['id']:
                return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Reviews.DoesNotExist:
            return Response({'msg': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        review.delete()
        Reviews.update_average_rating(review.restaurant.id)
        return Response({'message': 'Review delete'}, status=status.HTTP_204_NO_CONTENT)