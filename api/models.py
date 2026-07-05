from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Organizer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organizer_profile')
    company_name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(blank=True)
    websites = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return self.company_name

class Event(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.CharField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.event.title}" 

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='bookings')
    quantity = models.PositiveIntegerField(default=1)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket.name} - {self.ticket.event.title} *{self.quantity}"
    


