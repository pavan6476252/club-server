import asyncio
from asgiref.sync import sync_to_async
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Restos, Products
from .serializers import RestosSerializer, ProductSerializer, UserSerializer
from rest_framework.authentication import JWTAuthentication

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['uuid'] = str(user.uuid)
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class.request = request
        return super().post(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class UserSignupView(APIView):
    permission_classes = (AllowAny,)

    async def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = await sync_to_async(serializer.save)()
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(CustomTokenObtainPairView):
    permission_classes = (AllowAny,)

class UserLogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def post(self, request):
        refresh_token = request.data.get('refresh_token')
        authorization_header = request.headers.get('Authorization')

        if refresh_token or (authorization_header and authorization_header.startswith('Bearer ')):
            # Extract the refresh token from the request data or the Authorization header
            refresh_token = refresh_token or authorization_header.split(' ')[1]

            try:
                # Decode the refresh token to get the access token
                decoded_token = RefreshToken(refresh_token)
                access_token = decoded_token.access_token

                # Blacklist the access token
                await sync_to_async(access_token.blacklist)()

                return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
            except TokenError as e:
                return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)

class RestosViewSet(APIView):
    async def get(self, request, format=None):
        queryset = Restos.objects.all()
        membership = self.request.query_params.get('membership')
        if membership:
            queryset = queryset.filter(membership=membership)
        restos = queryset.order_by('-membership')
        serializer = RestosSerializer(restos, many=True)
        return Response(serializer.data)

class ProductList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request, format=None):
        resto_id = request.query_params.get('resto_id')
        queryset = Products.objects.filter(resto_id=resto_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
