from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/astronauts/', search_astronauts),  # GET
    path('api/astronauts/<int:astronaut_id>/', get_astronaut_by_id),  # GET
    path('api/astronauts/<int:astronaut_id>/update/', update_astronaut),  # PUT
    path('api/astronauts/<int:astronaut_id>/update_image/', update_astronaut_image),  # POST
    path('api/astronauts/<int:astronaut_id>/delete/', delete_astronaut),  # DELETE
    path('api/astronauts/create/', create_astronaut),  # POST
    path('api/astronauts/<int:astronaut_id>/add_to_flight/', add_astronaut_to_flight),  # POST

    # Набор методов для заявок
    path('api/flights/', search_flights),  # GET
    path('api/flights/<int:flight_id>/', get_flight_by_id),  # GET
    path('api/flights/<int:flight_id>/update/', update_flight),  # PUT
    path('api/flights/<int:flight_id>/update_status_user/', update_status_user),  # PUT
    path('api/flights/<int:flight_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/flights/<int:flight_id>/delete/', delete_flight),  # DELETE

    # Набор методов для м-м
    path('api/flights/<int:flight_id>/update_astronaut/<int:astronaut_id>/', update_astronaut_in_flight),  # PUT
    path('api/flights/<int:flight_id>/delete_astronaut/<int:astronaut_id>/', delete_astronaut_from_flight),  # DELETE

    # Набор методов пользователей
    path('api/users/register/', register), # POST
    path('api/users/login/', login), # POST
    path('api/users/logout/', logout), # POST
    path('api/users/<int:user_id>/update/', update_user) # PUT
]
