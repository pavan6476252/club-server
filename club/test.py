# import requests

# url = 'http://localhost:8000/api/login/'  # Replace 'your-api-url' with the actual URL of your API

# data = {
#     'username': 'karthik',
#     'password': 'karthik'
# }

# response = requests.post(url, data=data)
# print(response.status_code)

# if response.status_code == 200:
#     data = response.json()
#     token = data['token']
#     user = data['user']
#     # You can now use the token and user data for further requests or actions
#     print(f"Logged in successfully as {user['username']}")
#     print(f"Access token: {token}")
# else:
#     print("Login failed")
#     print(response.json())
# #=============logout 
# import requests

# url = 'http://localhost:8000/api/logout/'  # Replace 'your-api-url' with the actual URL of your API

# headers = {
#     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NjcyNTA3NywiaWF0IjoxNjg2NjM4Njc3LCJqdGkiOiJiM2FkZjIxMmNhYTk0MWYyYWM3OTU5MGVmMTBkYmU0YiIsInVzZXJfaWQiOjcsInV1aWQiOiI0MTIwZTA5NS0zZGFlLTRkMjEtOTA0NC0yZTgxMTgwNTlhMDUifQ.l4xjtag2B3Z9DWvjzzfYBTySxqqYzvL3LN7yIjDGPPg'
#     # Replace '<your-token>' with the actual JWT token obtained during login
# }

# response = requests.post(url, headers=headers)
# print(response.status_code)
# # print(response.content)
# if response.status_code == 200:
#     print("Logged out successfully")
# else:
#     print("Logout failed")
#     print(response.json())
# ======signup and automatic login


#otp
# import random
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView
# from msg91sms import MSG91

# @method_decorator(csrf_exempt, name='dispatch')
# class UserLoginView(TokenObtainPairView):
#     permission_classes = (AllowAny,)

#     def post(self, request, *args, **kwargs):
#         phone_number = request.data.get('phone_number')

#         # Generate OTP
#         otp = random.randint(100000, 999999)

#         # Send OTP using MSG91 API
#         msg91 = MSG91("YOUR_MSG91_AUTH_KEY")
#         msg91.send_otp(phone_number, otp)

#         # Save OTP in the User model
#         user, created = User.objects.get_or_create(phone_number=phone_number)
#         user.otp = otp
#         user.save()

#         return Response({'detail': 'OTP sent successfully.'})


# @method_decorator(csrf_exempt, name='dispatch')
# class OTPValidationView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request, *args, **kwargs):
#         phone_number = request.data.get('phone_number')
#         otp = request.data.get('otp')

#         # Retrieve User by phone number
#         user = User.objects.filter(phone_number=phone_number).first()

#         if not user:
#             return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

#         if otp != user.otp:
#             return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

#         # OTP validation successful, generate access and refresh tokens
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)

#         return Response({'access_token': access_token, 'refresh_token': str(refresh)})
