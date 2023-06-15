from django.urls import path
from .views import UserLoginView ,UserSignupView,UserLogoutView,RestosViewSet,ProductList,RestaurantSearch
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('Restos/',RestosViewSet.as_view(),name="Restos"),
    path('products/', ProductList.as_view(),name="products"),
    path('restaurants/', RestaurantSearch.as_view(), name='restaurant-search'),

    
]
