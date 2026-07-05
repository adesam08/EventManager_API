from django.urls import path
from . import views
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    #User Authentication
    path('register/buyer/', views.CreateBuyerView.as_view(), name='register-buyer'),
    path('register/organizer', views.CreateOrganizerView.as_view(), name='register-organizer'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),


    #Event
    path('api/events', views.ListEventAPIView.as_view(), name='events'),
    path('api/events/create', views.EventCreateAPIView.as_view(), name='create-events'),
    path('api/events/<str:pk>', views.EventRetrieveUpdateDestroyAPIView.as_view(), name='event-details'),
    path('api/events/<str:pk>/tickets', views.ListCreateTicketAPIView.as_view(), name='event-ticket'),
    path('api/events/<str:pk>/tickets/<str:ticket_pk>', views.TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-details')
    

]