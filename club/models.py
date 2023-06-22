from django.contrib.auth.models import AbstractUser,UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
import uuid
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class CustomUserManager(UserManager):
    pass

class User(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the form of +919999999999.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=6, null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return str(self.username) + str(self.uuid)

from django.contrib.auth import get_user_model
User = get_user_model()


class Customers(models.Model):
    uid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_membership = models.BooleanField()
    photo_url = models.CharField(max_length=255)
    location = models.CharField(max_length=255)


class RestoOwners(models.Model):
    uid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_membership = models.BooleanField()
    photo_url = models.CharField(max_length=255)
    location = models.CharField(max_length=255)


class Restos(models.Model):
    MEMBERSHIP_CHOICES = [
        ('0', 'normal'),
        ('1', 'Basic'),
        ('2', 'Standard'),
        ('3', 'Premium'),
    ]

    resto_id = models.BigAutoField(primary_key=True)
    uid = models.ForeignKey(RestoOwners, on_delete=models.CASCADE)
    resto_name = models.CharField(max_length=255)
    resto_mobile_number = models.CharField(max_length=255)
    resto_location = models.CharField(max_length=255)
    resto_certifications = models.CharField(max_length=255)
    view_rate = models.IntegerField()
    resto_registered_at = models.DateTimeField(auto_now_add=True)
    membership = models.CharField(choices=MEMBERSHIP_CHOICES, max_length=255, default='0')

    def __str__(self):
        return f"{str(self.resto_name)} - {str(self.resto_id)}"


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_person = models.CharField(max_length=255)
    booking_person_num1 = models.IntegerField()
    booking_person_num2 = models.IntegerField()
    event_category = models.CharField(max_length=255)
    crowd_count = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    booking_date = models.DateTimeField()


class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resto_id = models.ForeignKey(Restos, on_delete=models.CASCADE)


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    resto_id = models.ForeignKey(Restos, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.IntegerField()
    serves = models.IntegerField()
    product_discount = models.IntegerField()
    product_images = models.CharField(max_length=255)
    veg = models.BooleanField()
    product_category = models.CharField(max_length=255)
    def __str__(self):
        return f"{str(self.product_name)} - {str(self.product_id)}"



class Ratings(models.Model):
    rating_id = models.AutoField(primary_key=True)
    resto_id = models.ForeignKey(Restos, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField()
    timestamp = models.IntegerField()


class Promotions(models.Model):
    promotion_id = models.AutoField(primary_key=True)
    resto_id = models.ForeignKey(Restos, on_delete=models.CASCADE)
    promotion_price = models.IntegerField()
    promotion_banner = models.BinaryField()



class Bookings(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resto_id = models.ForeignKey(Restos, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    product_list = models.ManyToManyField(Products, through='BookingProduct')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.booking_id)

    def calculate_total_price(self):
        total_price = sum(
            booking_product.quantity * booking_product.product.product_price
            for booking_product in self.bookingproduct_set.all()
        )
        self.total_price = total_price
    def notify_resto_owner(self):
        channel_layer = get_channel_layer()
        group_name = f'resto_{self.resto_id.uid.uid}_owners'  # Modified to use resto_id.uid
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'notification_message',
                'booking_id': str(self.booking_id),
                'total_price': str(self.total_price),
                'user_data': {
                    'user_id': str(self.uid.id),
                    'username': self.uid.username,
                    'phone_number': self.uid.phone_number
                },
                'product_details': [
                    {
                        'product_id': str(booking_product.product.product_id),
                        'product_name': booking_product.product.product_name,
                        'quantity': booking_product.quantity
                    }
                    for booking_product in self.bookingproduct_set.all()
                ]
            }
        )
        print("step-1")

class BookingProduct(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.booking.booking_id} - {self.product.product_name} - {self.booking.uid.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resto_owner = models.ForeignKey(RestoOwners, on_delete=models.CASCADE)
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    status=models.CharField(max_length=255,null=True,default=None)
    message = models.CharField(max_length=255,null=True,default=None)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
