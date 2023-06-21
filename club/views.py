from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Restos,Products,Bookings,BookingProduct
# from club.models import User  # Import your custom User model
from .serializers import UserSerializer,RestosSerializer,ProductsSerializer,BookingsSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
import asyncio
from google.auth.transport import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from asgiref.sync import sync_to_async
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
import random,uuid
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
    return render(request,'index.html')




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

class Google_oauth(APIView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class.request = request

        # Retrieve the Google ID token from the request
        google_token = request.data.get('google_token')
        CLIENT_ID = '1082350793346-j6k8k71k21u5gpt4299sfukdk4hg7r98.apps.googleusercontent.com'  # Replace with your client ID

        try:
            # Verify the Google ID token
            id_info = id_token.verify_oauth2_token(google_token, requests.Request(), CLIENT_ID)

            # Retrieve or create the user based on the email
            user, created = User.objects.get_or_create(email=id_info['email'])

            # Generate the token pair
            refresh = self.get_token(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data)
        except ValueError:
            return Response({'detail': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)

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
class UserLoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')

        if username and password:
            # Authenticate with username/password
            user = authenticate(username=username, password=password)

            if user is None:
                return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        elif phone_number:
            # Generate OTP
            otp = random.randint(100000, 999999)

            # Send OTP using Twilio
            account_sid = 'AC8e6211196ebb5f125600af5880be86d0'
            auth_token = '1282dc84a3634ad65b474ba68df6a755'
            twilio_phone_number = '+14066938661'

            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f'Your OTP is: {otp}',
                from_=twilio_phone_number,
                to=phone_number
            )

            # Save OTP in the User model
            user, created = User.objects.get_or_create(phone_number=phone_number,username="Guest")
            user.otp = otp
            user.save()

        else:
            return Response({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if user is not None:
            return Response({'detail': 'OTP sent successfully.'})

        return Response({'detail': 'Invalid credentials or phone number.'}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='dispatch')
class OTPValidationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        # Retrieve User by phone number
        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if otp != user.otp:
            return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # OTP validation successful, generate access and refresh tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Clear OTP
        user.otp = None
        user.save()

        return Response({'access_token': access_token, 'refresh_token': str(refresh)})


class UserLogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
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
                access_token.blacklist()

                # Generate a new refresh token and access token
                new_refresh = RefreshToken.for_user(request.user)
                new_access = new_refresh.access_token

                return Response({
                    'refresh': str(new_refresh),
                    'access': str(new_access)
                }, status=status.HTTP_200_OK)
            except TokenError as e:
                return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)


class RestosViewSet(APIView):
    def get(self, request, format=None):
        queryset = Restos.objects.all()
        membership = self.request.query_params.get('membership')
        if membership:
            queryset = queryset.filter(membership=membership)
        restos = async_to_sync(self.order_queryset)(queryset)
        serializer = RestosSerializer(restos, many=True)
        return Response(serializer.data)

    async def order_queryset(self, queryset):
        # Perform any additional asynchronous operations on the queryset
        return queryset.order_by('-membership')
    
class ProductList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        resto_id = request.query_params.get('resto_id')
        queryset = Products.objects.filter(resto_id=resto_id)
        serializer = ProductsSerializer(queryset, many=True)
        return Response(serializer.data)




class RestaurantSearch(APIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        resto_name = request.query_params.get('resto_name', '')
        try:
            restaurant = Restos.objects.filter(resto_name__icontains=resto_name)
            serializer = RestosSerializer(restaurant, many=True)
            return Response(serializer.data, status=200)
        except Restos.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=404)

class BookingsAPIView(APIView):
    def post(self, request):
        serializer = BookingsSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            booking.calculate_total_price()  # Calculate total price

            # Get the user details who made the booking
            user = User.objects.get(uuid=booking.uid.uuid)
            user_data = {
                'user_id': user.uuid,
                'username': user.username,
                'phone_number': user.phone_number,  # Replace 'phone_number' with the actual field name
            }

            # Get the product details associated with the booking
            product_details = []
            booking_products = BookingProduct.objects.filter(booking=booking)
            for booking_product in booking_products:
                product_details.append({
                    'product_id': booking_product.product.product_id,
                    'product_name': booking_product.product.product_name,
                    'quantity': booking_product.quantity,
                    # Add other product details as needed
                })

            response_data = {
                'booking_id': booking.booking_id,
                'total_price': booking.total_price,
                'user_data': user_data,
                'product_details': product_details,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def csrf_failure_view(request, reason=""):
    # Your view logic here
    # Handle the CSRF failure and provide an appropriate response
    # You can customize the view based on your requirements
    return JsonResponse({"message": "CSRF verification failed."}, status=403)

