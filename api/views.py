from django.shortcuts import render, get_object_or_404
from .models import Event, Ticket, Booking
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .serializers import BookingSerializer, CreateUserSerializer, OrganizerUserSerializer, EventSerializer, CreateEventSerializer, TicketSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Organizer
from .filters import EventFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .permission import IsOrganizerOrReadOnly
from django.contrib.auth import get_user_model
User = get_user_model()

# User Authentication
class CreateBuyerView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

class CreateOrganizerView(generics.CreateAPIView):
    serializer_class = OrganizerUserSerializer
    permission_classes = [AllowAny]




# Other views
class EventCreateAPIView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = CreateEventSerializer
    

    def perform_create(self, serializer):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'organizer_profile'):
            organizer = self.request.user.organizer_profile
            serializer.save(organizer=organizer)
        else:
            raise PermissionDenied("Only organizers can create events.")
        
class ListEventAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
        
class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]

class ListCreateTicketAPIView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    def get_queryset(self):
        event_pk = self.kwargs['pk']
        return Ticket.objects.filter(event=event_pk)
    
    def perform_create(self, serializer):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        if event.organizer.user != self.request.user:
            raise PermissionError("You can only create ticket for your own Events")
        serializer.save()

class TicketRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    def get_object(self):
        event_pk = self.kwargs.get('pk')
        ticket_pk = self.kwargs.get('ticket_pk')

        return get_object_or_404(
            Ticket.objects.select_related('event'),
            pk=ticket_pk,
            event_id=event_pk,
        )
    
class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get('ticket_pk')
        ticket = get_object_or_404(Ticket, pk=ticket_id)

        if ticket.quantity_available < serializer.validated_data['quantity']:
            raise ValidationError("Ticket quantity exceeds available tickets.")

        serializer.save(user=self.request.user, ticket=ticket)
        ticket.quantity_available -= serializer.validated_data['quantity']
        ticket.save()




    
    







