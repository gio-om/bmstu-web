from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from orion.models import Astronaut, Flight, AstronautFlight


def index(request):
    astronaut_name = request.GET.get("astronaut_name", "")
    astronauts = Astronaut.objects.filter(status=1)

    if astronaut_name:
        astronauts = astronauts.filter(name__icontains=astronaut_name)

    draft_flight = get_draft_flight()

    context = {
        "astronaut_name": astronaut_name,
        "astronauts": astronauts
    }

    if draft_flight:
        context["astronauts_count"] = len(draft_flight.get_astronauts())
        context["draft_flight"] = draft_flight

    return render(request, "astronauts_page.html", context)


def add_astronaut_to_draft_flight(request, astronaut_id):
    astronaut = Astronaut.objects.get(pk=astronaut_id)

    draft_flight = get_draft_flight()

    if draft_flight is None:
        draft_flight = Flight.objects.create()
        draft_flight.owner = get_current_user()
        draft_flight.date_created = timezone.now()
        draft_flight.save()

    if AstronautFlight.objects.filter(flight=draft_flight, astronaut=astronaut).exists():
        return redirect("/")

    item = AstronautFlight(
        flight=draft_flight,
        astronaut=astronaut
    )
    item.save()

    return redirect("/")


def astronaut_details(request, astronaut_id):
    context = {
        "astronaut": Astronaut.objects.get(id=astronaut_id)
    }

    return render(request, "astronaut_page.html", context)


def delete_flight(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("UPDATE flights SET status=5 WHERE id = %s", [flight_id])

    return redirect("/")


def flight(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return redirect("/")

    flight = Flight.objects.get(id=flight_id)
    if flight.status == 5:
        return redirect("/")

    context = {
        "flight": flight,
    }

    return render(request, "flight_page.html", context)


def get_draft_flight():
    return Flight.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()