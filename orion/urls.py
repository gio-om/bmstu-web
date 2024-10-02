from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('astronauts/<int:astronaut_id>/', astronaut_details, name="astronaut_details"),
    path('astronauts/<int:astronaut_id>/add_to_flight/', add_astronaut_to_draft_flight, name="add_astronaut_to_draft_flight"),
    path('flights/<int:flight_id>/delete/', delete_flight, name="delete_flight"),
    path('flights/<int:flight_id>/', flight)
]
