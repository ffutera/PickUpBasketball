from django.urls import path

from . import views
 
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginuser, name="loginuser"),
    path("register", views.register, name="register"),
    path("verify", views.verify, name="verify"),
    path("logout", views.logoutuser, name="logoutuser"),
    path("portal", views.portal, name="portal"),
    path("cities", views.cities, name="cities"),
    path("pickups", views.pickups, name="pickups"),
    path("create/<int:country>/<int:city>", views.create, name="create"),
    path("add/<int:city>", views.addEvent, name="add"),
    path("event/<int:id>", views.event, name="event"),
    path("post/<int:id>",views.post,name="post"),
    path("going/<int:id>", views.going, name="going"),
    ]