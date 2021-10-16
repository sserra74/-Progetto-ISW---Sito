from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader

from .forms import RegisterUserForm, AddCameraForm, LoginUserForm, AddHotelForm, SearchForm
from .models import Camera, Prenotazione, Hotel
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
import json.encoder

# Create your views here.



#pagina principale dove l'utente non collegato può prenotare la stanza
def index(request):

    if (request.method == "POST"):
        form = SearchForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['citta']
            size = form.cleaned_data['postiletto']
            checkin = form.cleaned_data['checkin']
            checkout = form.cleaned_data['checkout']
            listaDisponibili = []
            for camera in Camera.objects.all():
                flag = False
                check = False
                if camera.posti_letto < int(float(size)) or camera.hotel.citta != city:
                    continue
                else:
                    for pren in Prenotazione.objects.all():
                        if pren.camera == camera:
                            new_checkin = datetime.strptime(checkin, "%Y-%m-%d")
                            new_checkout = datetime.strptime(checkout, "%Y-%m-%d")
                            pren_checkin = datetime.strptime(str(pren.checkin), "%Y-%m-%d")
                            pren_checkout = datetime.strptime(str(pren.checkout), "%Y-%m-%d")
                            if (pren_checkin <= new_checkin <= pren_checkout) or (
                                    pren_checkin <= new_checkout <= pren_checkout):
                                check = True
                            if new_checkin > new_checkout:
                                flag = True
                                break
                    if check is False:
                        listaDisponibili.append(camera)
                if flag == True:
                    break

            form = SearchForm()
            if (flag == True):
                context = {'dateError': True, 'form': form}
            elif (len(listaDisponibili) == 0):
                context = {'notAvailable': True, 'form': form}
            else:
                servizi = []
                for camera in listaDisponibili:
                    servizi.append(camera.servizi.split(", "))
                context = {'listaCamere': listaDisponibili, 'listaServizi': servizi, 'checkin': checkin,
                           'checkout': checkout, 'form': form}
        else:
            print("Form non valido - Search")
            context = {'searchFormError': True, 'form': form}
    else:
        form = SearchForm()
        context = {'form': form}
    return render(request, 'booking/index.html', context)

# #pagina di login
# def login(request):
#     return render(request, 'booking/login.html', {})

def registrazione(request):
    if (request.method == "POST"):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            newUser = form.save()
            albId = newUser .pk
            context = {'albid': albId}
            auth_login(request, newUser )
            #return render(request, 'booking/home.html', context)
            return redirect('/home/', context)
        else:
            print("Form non valido - Registrazione")
    else:
        form = RegisterUserForm()
        return render(request, 'booking/Registrazione.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('booking:home')
            else:
                context = {'loginerrato': True, 'form': form}
                return render(request, 'booking/login.html', context)
        else:
            context = {'formError': True, 'form': form}
            print("Form non valido - Registrazione")
            return render(request, 'booking/Registrazione.html', context)
    else:
        form = LoginUserForm()
        return render(request, 'booking/login.html', {'form': form})



def registrazione(request):
    return render(request, 'booking/Registrazione.html', {})

#submit del form di login, riporta alla home se login corretto o a loginerror se erratos
def hoteldetail(request):
    return render(request, 'booking/hoteldetail.html', {})


#riporta alla pagina di login mostrando un messaggio di errore
def loginError(request, loginErrato):
    context = {'loginerrato': loginErrato}
    return render(request, 'booking/login.html', context)

def search(request):
    city = request.POST.get("city", "")
    size = request.POST.get("size", "")
    checkin = request.POST.get("checkin", "")
    checkout = request.POST.get("checkout", "")
    listaDisponibili = []
    for camera in Camera.objects.all():
        flag = False
        check = False
        if camera.posti_letto < int(float(size)) or camera.hotel.citta != city:
            continue
        else:
            for pren in Prenotazione.objects.all():
                if pren.camera == camera:
                    new_checkin = datetime.strptime(checkin, "%Y-%m-%d")
                    new_checkout = datetime.strptime(checkout, "%Y-%m-%d")
                    pren_checkin = datetime.strptime(str(pren.checkin), "%Y-%m-%d")
                    pren_checkout = datetime.strptime(str(pren.checkout), "%Y-%m-%d")
                    if (pren_checkin <= new_checkin <= pren_checkout) or (pren_checkin <= new_checkout <= pren_checkout):
                        check = True
                    if new_checkin > new_checkout:
                        flag = True
                        break
            if check is False:
                listaDisponibili.append(camera)
        if flag==True:
            break

    if (flag == True):
        context = {'dateError': True}
    elif (len(listaDisponibili) == 0):
        context = {'notAvailable': True}
    else:
        servizi = []
        for camera in listaDisponibili:
            servizi.append(camera.servizi.split(", "))
        context = {'listaCamere': listaDisponibili, 'listaServizi': servizi, 'checkin': checkin,
                   'checkout': checkout}
    return render(request, 'booking/index.html', context)

#submit dell'email per la prenotazione, non avviene il refresh della pagina
def prenota(request):
    checkin = request.GET.get("checkin", "")
    checkout = request.GET.get("checkout", "")
    hotel = request.GET.get("hotel", "")
    camera = request.GET.get("camera", "")
    email = request.GET.get("email", "")
    hotelobj = Hotel.objects.get(nome=hotel)
    cameraobj = Camera.objects.get(hotel = hotelobj, numero=camera)
    newp = Prenotazione(email=email, camera=cameraobj, checkin=checkin, checkout=checkout)
    newp.save()
    return render(request, 'booking/index.html', {})

def manageCamera(request, hotel):
    if (request.method == "POST"):
        form = AddCameraForm(request.POST)
        if form.is_valid():

            posti_c = form.cleaned_data['posti_letto']
            numero_c = form.cleaned_data['numero']
            servizi_c = form.cleaned_data['servizi']

            all_servizi = ["Wifi", "Climatizzatore", "Tv", "Minifrigo"]
            check = False

            hotelObj = Hotel.objects.get(nome=hotel)
            citta = hotelObj.citta
            servizio = servizi_c.split(", ")

            alreadyexist = False
            checklength = Camera.objects.filter(hotel=hotelObj, numero=numero_c)
            if len(checklength) != 0:
                alreadyexist = True

            for serv in servizio:
                if (serv not in all_servizi or (len(servizio) != len(set(servizio)))):
                    check = True
                    break

            if not alreadyexist and not check:
                new_Camera = Camera.objects.create(hotel=hotelObj, numero=numero_c, posti_letto=posti_c, servizi=servizi_c)
                new_Camera.save()

            listaCamere = []
            for camera in Camera.objects.all():
                if camera.hotel == hotelObj:
                    listaCamere.append(camera)
            servizi = []
            for camera in listaCamere:
                servizi.append(camera.servizi.split(", "))

            form = AddCameraForm()

            if alreadyexist:
                context = {"hotel": hotel, "descrizione": hotelObj.descrizione, "indirizzo": hotelObj.indirizzo,
                           "listaCamere": listaCamere, "listaServizi": servizi, 'errorcamera': True, "citta": citta, 'form': form}
            elif check:
                context = {"hotel": hotel, "descrizione": hotelObj.descrizione, "indirizzo": hotelObj.indirizzo,
                           "listaCamere": listaCamere, "listaServizi": servizi, "erroreservizio": check, "citta": citta, 'form': form}
            else:
                context = {"hotel": hotel, "descrizione": hotelObj.descrizione, "indirizzo": hotelObj.indirizzo,
                           "listaCamere": listaCamere, "listaServizi": servizi, "citta": citta, 'form': form}

            return render(request, 'booking/hoteldetail.html', context)
        else:
            print("Form non valido - AddCameraDetail")
            hotelObj = Hotel.objects.get(nome=hotel)
            citta = hotelObj.citta

            listaCamere = []
            for camera in Camera.objects.all():
                if camera.hotel == hotelObj:
                    listaCamere.append(camera)
            servizi = []
            for camera in listaCamere:
                servizi.append(camera.servizi.split(", "))

            form = AddCameraForm()

            context = {"hotel": hotel, 'invalidForm': True, 'form': form, "descrizione": hotelObj.descrizione,
                       "indirizzo": hotelObj.indirizzo,
                       "listaCamere": listaCamere, "listaServizi": servizi, "citta": citta}
            return render(request, 'booking/hoteldetail.html', context)

    else:
        if request.user.is_authenticated:
            form = AddCameraForm()
            hotelObj = Hotel.objects.get(nome=hotel)
            descr = hotelObj.descrizione
            indirizzo = hotelObj.indirizzo
            citta = hotelObj.citta
            listaCamere = []
            for camera in Camera.objects.all():
                if camera.hotel == hotelObj:
                    listaCamere.append(camera)
            servizi = []
            for camera in listaCamere:
                servizi.append(camera.servizi.split(", "))

            context = {"hotel": hotel, "descrizione": descr, "indirizzo": indirizzo, "listaCamere": listaCamere,
                       "listaServizi": servizi, "citta": citta, 'form':form}
            return render(request, 'booking/hoteldetail.html', context)
        else:
            return redirect("booking:errorpage")




def manageHotel(request):
    if (request.method == "POST"):
        form = AddHotelForm(request.POST)
        if form.is_valid():
            print("Form valido - addHotel")
            nome_h = form.cleaned_data['nome']
            descrizione_h = form.cleaned_data["descrizione"]
            citta_h = form.cleaned_data["citta"]
            indirizzo_h = form.cleaned_data["indirizzo"]

            albId = request.user

            alreadyexist = False
            checklength = Hotel.objects.filter(nome=nome_h, proprietario=request.user)

            if len(checklength) != 0:
                alreadyexist = True
            else:
                newHotel = Hotel()
                newHotel.nome = nome_h
                newHotel.citta = citta_h
                newHotel.descrizione = descrizione_h
                newHotel.proprietario = request.user
                newHotel.indirizzo = indirizzo_h
                newHotel.save()

            allHotels = Hotel.objects.all()

            dict_Camera_Hotel = {}
            listaHotel = []

            for hotel in allHotels:
                if (hotel.proprietario == albId):
                    dict_Camera_Hotel[hotel.nome] = 0
                    listaHotel.append(hotel)

            for camera in Camera.objects.all():
                for hotel in listaHotel:
                    if (camera.hotel.nome == hotel.nome):
                        indice_camera = dict_Camera_Hotel[hotel.nome]
                        indice_camera += 1
                        dict_Camera_Hotel[hotel.nome] = indice_camera

            if alreadyexist:
                context = {'allHotels': allHotels, 'dictCamera': dict_Camera_Hotel, 'errorhotel': True, 'form':form}
            else:
                context = {'allHotels': allHotels, 'dictCamera': dict_Camera_Hotel, 'form':form}

            return render(request, 'booking/hotels.html', context)

        else:
            print("Form non valido - addHotel")
            # context = {'errorhotel': True}
            # return render(request, 'booking/hotels.html', context)
    else:
        form = AddHotelForm()
        if request.user.is_authenticated:
            allHotels = Hotel.objects.all()

            dict_Camera_Hotel = {}
            albId = request.user

            listaHotel = []

            for hotel in allHotels:
                if (hotel.proprietario == albId):
                    dict_Camera_Hotel[hotel.nome] = 0
                    listaHotel.append(hotel)

            for camera in Camera.objects.all():
                for hotel in listaHotel:
                    if (camera.hotel.nome == hotel.nome):
                        indice_camera = dict_Camera_Hotel[hotel.nome]
                        indice_camera += 1
                        dict_Camera_Hotel[hotel.nome] = indice_camera

            context = {'dictCamera': dict_Camera_Hotel,'form':form}

            return render(request, 'booking/hotels.html', context)
        else:
            return redirect("booking:errorpage")


def registraUtente(request):
    newEmail= request.POST.get("email", "")
    psw=request.POST.get("password", "")
    newNome=request.POST.get("nome", "")
    newCognome = request.POST.get("cognome", "")
    newUser=User.objects.create_user(username=newEmail,email=newEmail,password=psw)
    newUser.first_name=newNome
    newUser.last_name=newCognome
    newUser.save()

    albId = newUser.pk
    context={'albid': albId}
    auth_login(request, newUser)
    return render(request, 'booking/home.html', context)

def registrazione(request):
    if (request.method == "POST"):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            print("Form valido Registrazione")
            newUser = form.save()
            albId = newUser .pk
            context = {'albid': albId}
            auth_login(request, newUser)
            #return render(request, 'booking/home.html', context)
            return redirect('/home/', context)
        else:
            print("Form non valido - Registrazione")
    else:
        form = RegisterUserForm()
        return render(request, 'booking/Registrazione.html', {'form': form})


def errorpage(request):
    return render(request, 'booking/errorpage.html', {})

def errorpageredirect(request):
    if request.user.is_authenticated:
        # se l'utente è già autenticato devo mostrare la pagina home con le sue prenotazioni
        lista_Hotel = []
        lista_Camere = []
        lista_User = []

        albergatore = request.user

        for prenotazione in Prenotazione.objects.all():
            if (prenotazione.camera.hotel.proprietario == albergatore):
                lista_Hotel.append(prenotazione.camera.hotel)
                lista_Camere.append(prenotazione.camera.numero)
                lista_User.append(prenotazione.email)

        list = []
        for i in range(0, lista_Hotel.__len__()):
            list.append(i)

        context = {'albid': albergatore.pk, 'listaHotel': lista_Hotel, 'listaCamere': lista_Camere,
                   'listaUser': lista_User,
                   'length': list}
        return render(request, 'booking/home.html', context)
    else:
        return redirect("booking:index")

def home(request):
    if request.user.is_authenticated:

        lista_Hotel = []
        lista_Camere = []
        lista_User = []

        albergatore = request.user

        for prenotazione in Prenotazione.objects.all():
            if (prenotazione.camera.hotel.proprietario == albergatore):
                lista_Hotel.append(prenotazione.camera.hotel)
                lista_Camere.append(prenotazione.camera.numero)
                lista_User.append(prenotazione.email)

        list = []
        for i in range(0, lista_Hotel.__len__()):
            list.append(i)

        context = {'albid': albergatore.pk, 'listaHotel': lista_Hotel, 'listaCamere': lista_Camere,
                   'listaUser': lista_User,
                   'length': list}
        return render(request, 'booking/home.html', context)
    else:
        return redirect("booking:errorpage")


def logout(request):
    auth_logout(request)
    return redirect("booking:index")