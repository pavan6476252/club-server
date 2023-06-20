# import asyncio
# from asgiref.sync import sync_to_async
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from .models import Restos, Products
# from .serializers import RestosSerializer, ProductSerializer, UserSerializer
# from rest_framework.authentication import JWTAuthentication

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['uuid'] = str(user.uuid)
#         return token

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

#     def post(self, request, *args, **kwargs):
#         self.serializer_class.request = request
#         return super().post(request, *args, **kwargs)

# @method_decorator(csrf_exempt, name='dispatch')
# class UserSignupView(APIView):
#     permission_classes = (AllowAny,)

#     async def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = await sync_to_async(serializer.save)()
#             refresh = RefreshToken.for_user(user)
#             return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(csrf_exempt, name='dispatch')
# class UserLoginView(CustomTokenObtainPairView):
#     permission_classes = (AllowAny,)

# class UserLogoutView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     async def post(self, request):
#         refresh_token = request.data.get('refresh_token')
#         authorization_header = request.headers.get('Authorization')

#         if refresh_token or (authorization_header and authorization_header.startswith('Bearer ')):
#             # Extract the refresh token from the request data or the Authorization header
#             refresh_token = refresh_token or authorization_header.split(' ')[1]

#             try:
#                 # Decode the refresh token to get the access token
#                 decoded_token = RefreshToken(refresh_token)
#                 access_token = decoded_token.access_token

#                 # Blacklist the access token
#                 await sync_to_async(access_token.blacklist)()

#                 return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
#             except TokenError as e:
#                 return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response({'error': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)

# class RestosViewSet(APIView):
#     async def get(self, request, format=None):
#         queryset = Restos.objects.all()
#         membership = self.request.query_params.get('membership')
#         if membership:
#             queryset = queryset.filter(membership=membership)
#         restos = queryset.order_by('-membership')
#         serializer = RestosSerializer(restos, many=True)
#         return Response(serializer.data)

# class ProductList(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     async def get(self, request, format=None):
#         resto_id = request.query_params.get('resto_id')
#         queryset = Products.objects.filter(resto_id=resto_id)
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)


# from rest_framework import serializers
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import uuid

# from .models import Restos, User, Products, Bookings, BookingProduct


# class ProductsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Products
#         fields = '__all__'


# class BookingProductSerializer(serializers.ModelSerializer):
#     product = ProductsSerializer()

#     class Meta:
#         model = BookingProduct
#         fields = ('product', 'quantity')


# class BookingsSerializer(serializers.ModelSerializer):
#     product_list = BookingProductSerializer(many=True)

#     class Meta:
#         model = Bookings
#         fields = ('booking_id', 'resto_id', 'uid', 'booking_date', 'product_list')

#     def create(self, validated_data):
#         product_list_data = validated_data.pop('product_list')
#         booking = Bookings.objects.create(**validated_data)
#         for product_data in product_list_data:
#             product = product_data['product']
#             quantity = product_data['quantity']
#             BookingProduct.objects.create(booking=booking, product=product, quantity=quantity)
#         return booking


# class BookingsAPIView(APIView):
#     def post(self, request):
#         resto_id = request.data.get('resto_id')
#         user_id = request.data.get('user_id')
#         product_list = request.data.get('product_list')

#         if not (resto_id and user_id and product_list):
#             return Response({'error': 'resto_id, user_id, and product_list are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             resto = Restos.objects.get(pk=resto_id)
#             user = User.objects.get(pk=user_id)
#         except (Restos.DoesNotExist, User.DoesNotExist):
#             return Response({'error': 'Invalid resto_id or user_id.'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = BookingsSerializer(data={
#             'resto_id': resto,
#             'uid': user,
#             'product_list': product_list
#         })

#         if serializer.is_valid():
#             booking = serializer.save()
#             return Response({'booking_id': booking.booking_id}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
