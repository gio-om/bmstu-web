import random
import uuid
from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .permissions import *
from .redis import session_storage
from .serializers import *
from .utils import identity_user, get_session
from random import randint



def get_draft_flight(request):
    user = identity_user(request)

    if user is None:
        return None

    flight = Flight.objects.filter(owner=user).filter(status=1).first()

    return flight


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'query',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(["GET"])
def search_astronauts(request):
    astronaut_name = request.GET.get("astronaut_name", "")

    astronauts = Astronaut.objects.filter(status=1)

    if astronaut_name:
        astronauts = astronauts.filter(name__icontains=astronaut_name)

    serializer = AstronautsSerializer(astronauts, many=True)

    draft_flight = get_draft_flight(request)

    resp = {
        "astronauts": serializer.data,
        "astronauts_count": AstronautFlight.objects.filter(flight=draft_flight).count() if draft_flight else None,
        "draft_flight_id": draft_flight.pk if draft_flight else None
    }

    return Response(resp)


@api_view(["GET"])
def get_astronaut_by_id(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)
    serializer = AstronautSerializer(astronaut)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_astronaut(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)

    serializer = AstronautSerializer(astronaut, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_astronaut(request):
    serializer = AstronautSerializer(data=request.data, partial=False)

    serializer.is_valid(raise_exception=True)

    Astronaut.objects.create(**serializer.validated_data)

    astronauts = Astronaut.objects.filter(status=1)
    serializer = AstronautSerializer(astronauts, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsModerator])
def delete_astronaut(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)
    astronaut.status = 2
    astronaut.save()

    astronaut = Astronaut.objects.filter(status=1)
    serializer = AstronautSerializer(astronaut, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_astronaut_to_flight(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)

    draft_flight = get_draft_flight(request)

    if draft_flight is None:
        draft_flight = Flight.objects.create()
        draft_flight.date_created = timezone.now()
        draft_flight.owner = identity_user(request)
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
@permission_classes([IsModerator])
def update_astronaut_image(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)

    image = request.data.get("image")

    if image is None:
        return Response(status.HTTP_400_BAD_REQUEST)

    astronaut.image = image
    astronaut.save()

    serializer = AstronautSerializer(astronaut)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_flights(request):
    status_id = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    flights = Flight.objects.exclude(status__in=[1, 5])

    user = identity_user(request)
    if not user.is_superuser:
        flights = flights.filter(owner=user)

    if status_id > 0:
        flights = flights.filter(status=status_id)

    if date_formation_start and parse_datetime(date_formation_start):
        flights = flights.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        flights = flights.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = FlightsSerializer(flights, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_flight_by_id(request, flight_id):
    user = identity_user(request)

    if not Flight.objects.filter(pk=flight_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    serializer = FlightSerializer(flight)

    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=FlightSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_flight(request, flight_id):
    user = identity_user(request)

    if not Flight.objects.filter(pk=flight_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    serializer = FlightSerializer(flight, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, flight_id):
    user = identity_user(request)

    if not Flight.objects.filter(pk=flight_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)

    if flight.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    flight.status = 2
    flight.date_formation = timezone.now()
    flight.save()

    serializer = FlightSerializer(flight)

    return Response(serializer.data)


def random_date():
    now = datetime.now(tz=timezone.utc)
    return now + timedelta(random.uniform(-1, 0) * 100)

@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    flight = Flight.objects.get(pk=flight_id)

    if flight.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request_status == 3:
        flight.date = random_date()
        flight.is_successful = randint(0, 1)

    flight.status = request_status
    flight.date_complete = timezone.now()
    flight.moderator = identity_user(request)
    flight.save()

    serializer = FlightSerializer(flight)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_flight(request, flight_id):
    user = identity_user(request)

    if not Flight.objects.filter(pk=flight_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)

    if flight.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    flight.status = 5
    flight.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_astronaut_from_flight(request, flight_id, astronaut_id):
    user = identity_user(request)

    if not Flight.objects.filter(pk=flight_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not AstronautFlight.objects.filter(flight_id=flight_id, astronaut_id=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = AstronautFlight.objects.get(flight_id=flight_id, astronaut_id=astronaut_id)
    item.delete()

    flight = Flight.objects.get(pk=flight_id)

    serializer = FlightSerializer(flight)
    astronauts = serializer.data["astronauts"]

    return Response(astronauts)


@swagger_auto_schema(method='PUT', request_body=AstronautFlightSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_astronaut_in_flight(request, flight_id, astronaut_id):
    user = identity_user(request)

    if not Flight.objects.filter(pk=flight_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not AstronautFlight.objects.filter(astronaut_id=astronaut_id, flight_id=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = AstronautFlight.objects.get(astronaut_id=astronaut_id, flight_id=flight_id)

    serializer = AstronautFlightSerializer(item, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    user = identity_user(request)

    if user is not None:
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    session_id = str(uuid.uuid4())
    session_storage.set(session_id, user.id)

    serializer = UserSerializer(user)
    response = Response(serializer.data, status=status.HTTP_200_OK)
    response.set_cookie("session_id", session_id, samesite="lax")

    return response


@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    session_id = str(uuid.uuid4())
    session_storage.set(session_id, user.id)

    serializer = UserSerializer(user)
    response = Response(serializer.data, status=status.HTTP_201_CREATED)
    response.set_cookie("session_id", session_id, samesite="lax")

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    session = get_session(request)
    session_storage.delete(session)

    response = Response(status=status.HTTP_200_OK)
    response.delete_cookie('session_id')

    return response


@swagger_auto_schema(method='PUT', request_body=UserProfileSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = identity_user(request)

    if user.pk != user_id:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    password = request.data.get("password", None)
    if password is not None and not user.check_password(password):
        user.set_password(password)
        user.save()

    return Response(serializer.data, status=status.HTTP_200_OK)
