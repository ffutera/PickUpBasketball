from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
	    return f"{self.name}"

class Location(models.Model):
	name = models.CharField(max_length=100)
	country = models.ForeignKey(Country, null=False, on_delete = models.CASCADE, related_name="country", blank = False )
	def __str__(self):
		return f"{self.name}, {self.country}"

class Event(models.Model):
	name = models.CharField(max_length=75)
	city = models.ForeignKey(Location, null=False, on_delete=models.CASCADE, related_name="city",blank=False)
	date = models.DateField(default=date.today)
	address = models.CharField(max_length=75)
	attendees = models.FloatField(default=1)
	occured = models.IntegerField(default=False)
	going = models.ManyToManyField(User)
	def __str__(self):
		return f"{self.name}"

class Message(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message", blank=False)
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event", blank=False)
	date = models.DateField(default=date.today)
	content = models.CharField(max_length=75)
	def __str__(self):
		return f"{self.author}, {self.date}"

	