from django.contrib import admin
from .models import *

class EventInline(admin.TabularInline):
    model = Event

class CityAdmin(admin.ModelAdmin):
    inlines = [EventInline]

# Register your models here.    
admin.site.register(Country)
admin.site.register(Location, CityAdmin)
admin.site.register(Event)
admin.site.register(Message)