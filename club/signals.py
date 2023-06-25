from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bookings, Notification
import pdb

@receiver(post_save, sender=Bookings)
def booking_post_save(sender, instance, created, **kwargs):
    if created:
        print("created")
        notification = Notification.objects.create(
            user=instance.uid,
            resto_owner=instance.resto_id.uid,
            booking=instance,
            status='PENDING',
            message='New booking request',
        )
        instance.calculate_total_price()
        instance.notify_resto_owner()
    else:
        # Update the notification status when a booking is updated
        notification = Notification.objects.get(booking=instance)
        if instance.status == 'ACCEPTED':
            notification.status = 'ACCEPTED'
            notification.message = 'Booking request accepted'
        elif instance.status == 'REJECTED':
            notification.status = 'REJECTED'
            notification.message = 'Booking request rejected'
        notification.save()
