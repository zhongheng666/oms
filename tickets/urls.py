from django.urls import path
from .views import TicketCreateView, load_floors, load_incidents, MyTicketsView

urlpatterns = [
    path('', TicketCreateView.as_view(), name='ticket_dashboard'),
    path('create/', TicketCreateView.as_view(), name='ticket_create'),
    path('load-floors/', load_floors, name='load_floors'),
    path('load-incidents/', load_incidents, name='load_incidents'),
    path('my-tickets/', MyTicketsView.as_view(), name='my_tickets'),
]
