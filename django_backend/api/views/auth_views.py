import bcrypt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User
from ..serializers import RegisterSerializer, LoginSerializer, UserSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken()
    refresh['id'] = user.id
    refresh['username'] = user.username
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        username = data['username']
        email = data['email']
        password = data['password']

        if User.objects.filter(username=username).exists():
            return Response({'message': 'User already exists', 'details': 'Username is taken'}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({'message': 'User already exists', 'details': 'Email is already registered'}, status=400)

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(username=username, email=email, password=hashed)

        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'User registered successfully',
            'token': tokens['access'],
            'user': {'id': user.id, 'username': user.username, 'email': user.email}
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response({'message': 'Invalid username or password'}, status=400)

        if not bcrypt.checkpw(data['password'].encode(), user.password.encode()):
            return Response({'message': 'Invalid username or password'}, status=400)

        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Login successful',
            'token': tokens['access'],
            'user': {'id': user.id, 'username': user.username, 'email': user.email}
        })


class MeView(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'message': 'No token provided'}, status=401)

        token_str = auth_header.split(' ')[1]
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            token = AccessToken(token_str)
            user_id = token.get('id')
            user = User.objects.get(id=user_id)
        except Exception:
            return Response({'message': 'Invalid token'}, status=401)

        return Response({'user': {'id': user.id, 'username': user.username, 'email': user.email}})
