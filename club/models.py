# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.core.validators import RegexValidator

class User(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    phone_regex = RegexValidator( regex = r'^\+?1?\d{9,14}$', message = "Phone number must be entered in the form of +919999999999.")
    phone_number = models.CharField(validators=[phone_regex],max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add any other fields or methods you need

    def __str__(self):
        return self.uuid


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
        ('0','normal'),
        ('1', 'Basic'),
        ('2', 'Standard'),
        ('3', 'Premium'),
    ]

    resto_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(RestoOwners, on_delete=models.CASCADE)
    resto_name = models.CharField(max_length=255)
    resto_mobile_number = models.CharField(max_length=255)
    resto_location = models.CharField(max_length=255)
    resto_certifications = models.CharField(max_length=255)
    view_rate = models.IntegerField()
    resto_registered_at = models.DateTimeField(auto_now_add=True)
    membership = models.CharField(choices=MEMBERSHIP_CHOICES, max_length=255,default=0)


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



class Bookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    resto_id = models.ForeignKey(Restos, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    product_list = models.JSONField(default=None)

    def __str__(self):
        return str(self.booking_id)




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