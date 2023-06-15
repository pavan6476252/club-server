from django.contrib import admin
from .models import User, Customers, RestoOwners, Restos, Events, Posts, Bookings, Products, Ratings, Promotions

admin.site.register(User)
admin.site.register(Customers)
admin.site.register(RestoOwners)
admin.site.register(Restos)
admin.site.register(Events)
admin.site.register(Posts)
admin.site.register(Bookings)
admin.site.register(Products)
admin.site.register(Ratings)
admin.site.register(Promotions)
