from django.urls import path, include
from .views import UserLoginView, UserSignupView, UserLogoutView, RestosViewSet, ProductList, RestaurantSearch, OTPValidationView, home, Google_oauth, BookingsAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import routing

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('google-login/', Google_oauth.as_view(), name='google-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('Restos/', RestosViewSet.as_view(), name="Restos"),
    path('products/', ProductList.as_view(), name="products"),
    path('restaurants/', RestaurantSearch.as_view(), name='restaurant-search'),
    path('validate-otp/', OTPValidationView.as_view(), name="otp-validation"),
    path('bookings/', BookingsAPIView.as_view(), name='bookings'),
    path('home/', home, name="apis-description"),
    path('ws/', include(routing.websocket_urlpatterns)),
]
