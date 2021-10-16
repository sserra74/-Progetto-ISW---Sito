from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "booking"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("login/<slug:loginErrato>", views.loginError, name="loginErrato"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("hotels/", views.manageHotel, name='hotels'),
    path("hoteldetail/<str:hotel>", views.manageCamera, name="hoteldetail"),
    path("#", views.search, name="search"),
    path("#c", views.prenota, name="prenota"),
    path("registrazione/#", views.registraUtente, name="registraUtente"),
    path("registrazione/", views.registrazione, name="registrazione"),
    path("errorpage", views.errorpage, name="errorpage"),
    path("errorpage/#", views.errorpageredirect, name="errorpageredirect")
]