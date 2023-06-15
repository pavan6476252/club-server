from django.urls import path
from .views import UserLoginView ,UserSignupView,UserLogoutView,RestosViewSet,ProductList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('home/',RestosViewSet.as_view(),name="hello"),
    path('products/', ProductList.as_view(),name="products"),
    
]
