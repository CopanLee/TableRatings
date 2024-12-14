import hashlib

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Users
from .serializers import RegisterSerializer


class RegisterAPI(APIView):

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: 'Registered'},
        security=[]
    )
    def post(self, request):
        """
        Register
        """
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        # Get the username and password from the request
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        name = serializer.validated_data['name']
        phone = serializer.validated_data['phone']
        email = serializer.validated_data['email']
        # hash the password
        password = hashlib.sha256(password.encode()).hexdigest()
        # Check if the username is already exists
        if Users.objects.filter(username=username).exists():
            return Response({'msg': 'Username already exists'}, status=400)
        # Create a new user
        user = Users(username=username, password=password, name=name, phone=phone, email=email)
        user.save()
        return Response({'msg': 'Registered'}, status=201)
