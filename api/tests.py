from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from .models import Event, Organizer, Ticket

User = get_user_model()


class TicketNestedRouteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='organizer@example.com',
            email='organizer@example.com',
            password='password',
        )
        self.organizer = Organizer.objects.create(user=self.user, company_name='Acme')
        self.event = Event.objects.create(
            organizer=self.organizer,
            title='Test Event',
            description='A test event',
            location='Lagos',
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=2),
        )
        self.ticket = Ticket.objects.create(
            event=self.event,
            name='VIP',
            price='50.00',
            quantity_available=10,
        )

    def test_ticket_can_be_updated_with_nested_url(self):
        self.client.force_authenticate(self.user)
        url = reverse('ticket-details', args=[self.event.pk, self.ticket.pk])

        response = self.client.put(
            url,
            {'event': self.event.pk, 'name': 'Standard', 'price': '30.00', 'quantity_available': 8},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.name, 'Standard')

    def test_ticket_can_be_deleted_with_nested_url(self):
        self.client.force_authenticate(self.user)
        url = reverse('ticket-details', args=[self.event.pk, self.ticket.pk])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Ticket.objects.filter(pk=self.ticket.pk).exists())
