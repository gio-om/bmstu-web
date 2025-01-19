from django.contrib import admin

from .models import *

admin.site.register(Astronaut)
admin.site.register(Flight)
admin.site.register(AstronautFlight)
