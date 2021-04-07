from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from django.core.mail import send_mail
from datetime import datetime

# Create your views here.

def index(request):   
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": ""})
    else: 
        return HttpResponseRedirect(reverse("portal"))

def loginuser(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid Credentials."})

def register(request):
    if not request.user.is_authenticated:
        return render(request, "users/register.html", {"message": ""})
    else: 
        return HttpResponseRedirect(reverse("index"))

def verify(request):
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    if (User.objects.filter(username=username).exists()):
        return render(request, "users/register.html", {"message": "Username Taken!"})
    if (User.objects.filter(email=email).exists()):
        return render(request, "users/register.html", {"message": "Email Taken!"})
    if (email.count('@') == 0 ):
    	return render(request, "users/register.html", {"message": "Invalid email address"})
    else:
        user = User.objects.create_user(username, email, password)
        return HttpResponseRedirect(reverse("index"))

def logoutuser(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

def portal(request):
    countries = Country.objects.all().order_by('name')
    cities = countries[0].country.all().order_by('name')
    info = {
    "username": request.user.username,
    "countries": countries,
    "cities": cities,
    }
    return render(request, "algorithm/portal.html", info)

def cities(request):
    data = request.GET['country']
    print(data)
    country = Country.objects.all().filter(name=data)
    cities = country[0].country.all().order_by('name')
    temp = []
    for city in cities:
        temp.append(city.name)
    #print("cities: ", temp) 
    return JsonResponse({'cities': temp})

def pickups(request):
    country = Country.objects.all().filter(name=request.POST['nations'])[0]
    init = Location.objects.all().filter(name=request.POST['cities'])
    if (len(list(init)) == 0):
        city = country.country.all().order_by('name')[0]
    else:
        city = init[0]
    if request.POST.get('submit') == "Create Event":
        return HttpResponseRedirect(reverse("create", args=(country.id,city.id,)))
    startdate = date.today()
    enddate = datetime(3000,12,30)
    try:
        fltr = request.POST['sort']
        if fltr == "popularity":
            events = city.city.all().order_by('attendees').filter(date__range=[startdate, enddate])
        else:
            events = city.city.all().order_by('date').filter(date__range=[startdate, enddate])
    except TypeError:
        events = city.city.all().order_by('date').filter(date__range=[startdate, enddate])
    info = {
    "user": request.user,
	"username": request.user.username,
	"events": events,
    "country": country.name,
    "city": city.name,
    }
    return render(request, "algorithm/pickup.html", info)

def create(request, country, city):
    country = Country.objects.get(pk=country)
    city = Location.objects.get(pk=city)
    month = datetime.now().month
    if month<10:
        month = "0{month}".format(month=datetime.now().month)
    fDate = "{year}-{month}-{day}".format(year=datetime.now().year,month=month,day=datetime.now().day) 
    return render(request, "algorithm/create.html", {"country": country, "city":city, "date":fDate})

def addEvent(request,city):
    name = request.POST['name']
    address = request.POST['address']
    date = request.POST['event-date']
    try:
        date = datetime(year= int(date[0:4]), month= int(date[5:7]), day= int(date[9:11]))
    except ValueError:
        city = Location.objects.get(pk=city)
        month = datetime.now().month
        if month<10:
            month = "0{month}".format(month=datetime.now().month)
        fDate = "{year}-{month}-{day}".format(year=datetime.now().year,month=month,day=datetime.now().day) 
        return render(request, "algorithm/create.html", {"city":city, "date":fDate, "message":"Invalid date! Try again!",})
    Event.objects.create(name=name, address=address, city=Location.objects.get(pk=city), date = date)
    return HttpResponseRedirect(reverse("portal"))

def event(request,id):
    event = Event.objects.get(pk=id)
    messages = event.event.all().order_by('date')
    user = request.user
    if user in event.going.all():
        boolean = True
    else:
        boolean = False
    return render(request, "algorithm/event.html",{"event":event,"username": request.user.username,"messages":messages, "user":user, "bool":boolean})

def post(request, id):
    message = request.POST['message']
    Message.objects.create(author=request.user, content=message, event=Event.objects.get(pk=id))
    return HttpResponseRedirect(reverse("event",args=[id]))

def going(request, id):
    event = Event.objects.get(pk=id)
    event.attendees +=1
    event.going.add(request.user)
    event.save()
    return HttpResponseRedirect(reverse("event",args=[id]))
# Create your views here.
