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
import requests

url = 'http://localhost:8000/api/logout/'  # Replace 'your-api-url' with the actual URL of your API

headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NjcyNTA3NywiaWF0IjoxNjg2NjM4Njc3LCJqdGkiOiJiM2FkZjIxMmNhYTk0MWYyYWM3OTU5MGVmMTBkYmU0YiIsInVzZXJfaWQiOjcsInV1aWQiOiI0MTIwZTA5NS0zZGFlLTRkMjEtOTA0NC0yZTgxMTgwNTlhMDUifQ.l4xjtag2B3Z9DWvjzzfYBTySxqqYzvL3LN7yIjDGPPg'
    # Replace '<your-token>' with the actual JWT token obtained during login
}

response = requests.post(url, headers=headers)
print(response.status_code)
# print(response.content)
if response.status_code == 200:
    print("Logged out successfully")
else:
    print("Logout failed")
    print(response.json())
# ======signup and automatic login