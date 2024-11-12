import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


def get_draft_flight():
    return Flight.objects.filter(status=1).first()


def get_user():
    return User.objects.filter(is_superuser=False).first()


def get_moderator():
    return User.objects.filter(is_superuser=True).first()


# МЕТОДЫ АСТРОНАВТОВ
@api_view(["GET"])
def search_astronauts(request):
    """
    Получение списка астронавтов с фильтром
    """
    astronaut_name = request.GET.get("astronaut_name", "")

    astronauts = Astronaut.objects.filter(status=1)

    if astronaut_name:
        astronauts = astronauts.filter(name__icontains=astronaut_name)

    serializer = AstronautSerializer(astronauts, many=True)

    draft_flight = get_draft_flight()

    resp = {
        "astronauts": serializer.data,
        "draft_flight": draft_flight.pk if draft_flight else None,
        "astronauts_count": AstronautFlight.objects.filter(flight=draft_flight).count() if draft_flight else None
    }

    return Response(resp)


@api_view(["GET"])
def get_astronaut_by_id(request, astronaut_id):
    """
    Получение астронавта по id
    """
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)
    serializer = AstronautSerializer(astronaut, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_astronaut(request, astronaut_id):
    """
    Обновление данных астронавта
    """
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)

    serializer = AstronautSerializer(astronaut, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_astronaut(request):
    """
    Создание пустого астронавта и вывод всех
    """
    Astronaut.objects.create(space_time=0)

    astronauts = Astronaut.objects.filter(status=1)
    serializer = AstronautSerializer(astronauts, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_astronaut(request, astronaut_id):
    """
    Удаление астронавта по id и вывод всех 
    """
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)
    astronaut.status = 2
    astronaut.save()

    astronauts = Astronaut.objects.filter(status=1)
    serializer = AstronautSerializer(astronauts, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_astronaut_to_flight(request, astronaut_id):
    """
    Добавление астронавта в полет и вывод экипажа(создает полет, если нет) 
    """
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)

    draft_flight = get_draft_flight()

    if draft_flight is None:
        draft_flight = Flight.objects.create()
        draft_flight.owner = get_user()
        draft_flight.date_created = timezone.now()
        draft_flight.save()

    if AstronautFlight.objects.filter(flight=draft_flight, astronaut=astronaut).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    item = AstronautFlight.objects.create()
    item.flight = draft_flight
    item.astronaut = astronaut
    item.save()

    serializer = FlightSerializer(draft_flight)
    return Response(serializer.data["astronauts"])


@api_view(["POST"])
def update_astronaut_image(request, astronaut_id):
    """
    Обновление картинки астронавта
    """
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)

    image = request.data.get("image")
    if image is not None:
        astronaut.image = image
        astronaut.save()

    serializer = AstronautSerializer(astronaut)

    return Response(serializer.data)



# МЕТОДЫ ПОЛЕТА
@api_view(["GET"])
def search_flights(request):
    """
    Получение полетов и фильтрация по статусу и дате
    """
    status = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    flights = Flight.objects.exclude(status__in=[5]) # Без удаленных

    if status > 0:
        flights = flights.filter(status=status)

    if date_formation_start and parse_datetime(date_formation_start):
        flights = flights.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        flights = flights.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = FlightsSerializer(flights, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_flight_by_id(request, flight_id):
    """
    Получение полета со списком астронавтов
    """
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    serializer = FlightSerializer(flight, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_flight(request, flight_id):
    """
    Изменение данных полета
    """
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    serializer = FlightSerializer(flight, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, flight_id):
    """
    Формирование полета пользователем
    """
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)

    if flight.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    flight.status = 2
    flight.date_formation = timezone.now()
    flight.save()

    serializer = FlightSerializer(flight, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, flight_id):
    """
    Завершение/Отклонение полета модератором
    """
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 5]:  # Или отклоняем(3) или завершаем(5)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    flight = Flight.objects.get(pk=flight_id)

    if flight.status != 2:  # Если статус полета "в работе" (2)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    flight.date_complete = timezone.now()
    flight.status = request_status
    flight.moderator = get_moderator()
    flight.save()

    serializer = FlightSerializer(flight, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_flight(request, flight_id):
    """
    Удаление полета
    """
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)

    if flight.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    flight.status = 5
    flight.save()

    serializer = FlightSerializer(flight, many=False)

    return Response(serializer.data)


# МЕТОДЫ М-М
@api_view(["DELETE"])
def delete_astronaut_from_flight(request, flight_id, astronaut_id):
    """
    Удалить астронавта из полета
    """
    if not AstronautFlight.objects.filter(flight_id=flight_id, astronaut_id=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = AstronautFlight.objects.get(flight_id=flight_id, astronaut_id=astronaut_id)
    item.delete()

    flight = Flight.objects.get(pk=flight_id)

    serializer = FlightSerializer(flight, many=False)
    astronauts = serializer.data["astronauts"]

    if len(astronauts) == 0:
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(astronauts)


@api_view(["PUT"])
def update_astronaut_in_flight(request, flight_id, astronaut_id):
    """
    Изменить значение поля в м-м
    """
    if not AstronautFlight.objects.filter(astronaut_id=astronaut_id, flight_id=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = AstronautFlight.objects.get(astronaut_id=astronaut_id, flight_id=flight_id)

    serializer = AstronautFlightSerializer(item, data=request.data,  partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)



# МЕТОДЫ ПОЛЬЗОВАТЕЛЯ
@api_view(["POST"])
def register(request):
    """
    Регистрация (Создание нового пользователя)
    """
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_user(request, user_id):
    """
    Обновление данных пользователя (Личный кабинет)
    """
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(pk=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def login(request):
    """
    Аутентификация
    """
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout(request):
    """
    Деавторизация
    """
    return Response(status=status.HTTP_200_OK)
