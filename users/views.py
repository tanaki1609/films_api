from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView

from .serializers import UserCreateSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def register_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.create_user(username=username, password=password,
                                    email=email, is_active=False)
    # create code (6-symbol)
    # send to email
    return Response({'success': 'User created successfully'},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
def confirm_user_api_view(request):
    pass


class AuthAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
