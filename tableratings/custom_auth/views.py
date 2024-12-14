import hashlib

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from users.models import Users

from .serializers import LoginSerializer


class LoginAPI(APIView):

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={204: 'Logged in'},
        security=[]
    )
    def post(self, request):
        """
        Login
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        # hash the password
        password = hashlib.sha256(password.encode()).hexdigest()
        # Check if the username and password are correct with sql
        queryset = Users.objects.filter(username=username, password=password)
        if queryset.exists():
            # if the username and password are correct, generate JWT token
            user = queryset.first()
            token = AccessToken.for_user(user)
            # set the token in the cookie
            response = Response({'msg': 'Logged in'}, status=204)
            response.set_cookie('Authorization', f'{token}')
            return response
        else:
            return Response({'message': 'Username or password uncorrect'}, status=401)
