import unittest
from datetime import datetime

from django.test import Client
from django.contrib.auth.models import User
from django.test import TestCase
from .models import *
from django.contrib.auth import authenticate
from .models import Camera, Hotel, Prenotazione

# Create your tests here.

class HotelTest(TestCase):

    def createUser(self):
        p1 = User.objects.create(username="prova1", email="prova1", password="prova1")
        return p1

    def createHotel(self):
        p1 = User.objects.create(username="prova1", email="prova1", password="prova1")
        h1 = Hotel.objects.create(nome="La Stella", descrizione="La Stella",
                                  citta="Roma", indirizzo="Via Roma 1", proprietario=p1)
        return h1

    def createAnotherHotel(self):
        p1 = User.objects.create(username="prova2", email="prova2", password="prova2")
        h1 = Hotel.objects.create(nome="La Luna", descrizione="La Luna",
                                  citta="Roma", indirizzo="Via Roma 2", proprietario=p1)
        return h1

    def getHotelOwner(self, hotel):
        return hotel.proprietario

    #controlla se viene creato l'hotel
    def testCreateHotel(self):
        self.assertTrue(self.createHotel())

    #controlla se la funzione str dell'Hotel restituisce il nome
    def testHotelStringName(self):
        h1 = self.createHotel()
        self.assertEqual(h1.__str__(), h1.nome)

    #controlla che l'hotel creato sia un'istanza di hotel
    def testHotelInstance(self):
        h1 = self.createHotel()
        self.assertIsInstance(h1, Hotel)

    #controlla se due hotel creati hanno proprietario diverso
    def testHotelOwner(self):
        h1 = self.createHotel()
        h2 = self.createAnotherHotel()
        self.assertIsNot(self.getHotelOwner(h1), self.getHotelOwner(h2))

    #controlla se il nome della classe sia con il plurale giusto
    def testHotelVerbosePlural(self):
        self.assertEqual(str(Hotel._meta.verbose_name_plural), "hotels")

    #controlla che il prorpietario dell'hotel venga veramente modificato
    def testChangeHotelOwner(self):
        h1 = self.createHotel()
        oldOwner = h1.proprietario
        p1 = User.objects.create(username="mario@gmail.com", email="mario@gmail.com", password="mario")
        h1.proprietario = p1
        self.assertNotEqual(h1.proprietario, oldOwner)

    #controlla se la città di un'hotel viene cambiata correttamente
    def testChangeHotelCity(self):
        h1 = self.createHotel()
        oldCity = h1.citta
        h1.citta = "Lucca"
        self.assertNotEqual(h1.citta, oldCity)

    #controlla se l'indirizzo di un hotel viene cambiato correttamente
    def testChangeHotelAddress(self):
        h1 = self.createHotel()
        oldAddress = h1.indirizzo
        h1.indirizzo = "Via Liguria 5"
        self.assertNotEqual(h1.indirizzo, oldAddress)

    def testHotelName(self):
        h1=self.createHotel()
        with self.assertRaises(Exception) as message:
            print(message)
            self.createHotel()




class CameraTest(TestCase):

    def createOtherHotel(self):
        u = User.objects.create(username="provaO", email="provaO", password="provaO")
        h = Hotel.objects.create(nome="La Prova", descrizione="La Prova",
                                  citta="Milano", indirizzo="Via Milano 1", proprietario=u)
        return h

    def createCamera(self):
        p1 = User.objects.create(username="prova1", email="prova1", password="prova1")
        h1 = Hotel.objects.create(nome="La Stella", descrizione="La Stella",
                                  citta="Roma", indirizzo="Via Roma 1", proprietario=p1)
        c1 = Camera.objects.create(hotel=h1, numero=1, posti_letto=5, servizi="Condizionatore")
        return c1

    def createAnotherCameraSameHotel(self):
        p1 = User.objects.create(username="prova1", email="prova1", password="prova1")
        h1 = Hotel.objects.create(nome="La Stella", descrizione="La Stella",
                                  citta="Roma", indirizzo="Via Roma 1", proprietario=p1)
        c1 = Camera.objects.create(hotel=h1, numero=2, posti_letto=6, servizi="Condizionatore")
        return c1

    def createAnotherCameraDiffHotel(self):
        p1 = User.objects.create(username="prova1", email="prova1", password="prova1")
        h1 = Hotel.objects.create(nome="La Luna", descrizione="La Luna",
                                  citta="Roma", indirizzo="Via Roma 2", proprietario=p1)
        c1 = Camera.objects.create(hotel=h1, numero=1, posti_letto=5, servizi="Condizionatore")
        return c1

    # controlla se viene creato la camera
    def testCameraInstance(self):
        c1 = self.createCamera()
        self.assertIsInstance(c1, Camera)

    def testCreateCamera(self):
        self.assertTrue(self.createCamera())

    # controlla se il nome della classe sia con il plurale giusto
    def testCameraVerbosePlural(self):
        self.assertEqual(str(Camera._meta.verbose_name_plural), "camere")

    def testEqualCamera(self):
        c1 = self.createCamera()
        self.assertNotEqual(Camera.objects.filter(numero=c1.numero, hotel=c1.hotel).count(), 0)

    def testPreviousInsertCamera(self):
        p1 = User.objects.create(username="prova3", email="prova3", password="prova1")
        h1 = Hotel.objects.create(nome="La Stella", descrizione="La Stella",
                                  citta="Roma", indirizzo="Via Roma 1", proprietario=p1)
        c1 = Camera(hotel=h1, numero=8, posti_letto=5, servizi="Condizionatore")
        self.assertEqual(Camera.objects.filter(numero=c1.numero, hotel=c1.hotel).count(), 0)

    def testServiceCameraNotFound(self):
        p1 = User.objects.create(username="prova3", email="prova3", password="prova1")
        h1 = Hotel.objects.create(nome="La Stella", descrizione="La Stella",
                                  citta="Roma", indirizzo="Via Roma 1", proprietario=p1)
        c1 = Camera(hotel=h1, numero=8, posti_letto=5, servizi="Aspirapolvere")

        listaPossibili = ["Climatizzatore", "Wifi", "Tv", "Minifrigo"]

        serviziSelected = []
        serviziSelected = c1.servizi.split(", ")
        check = True

        for servizio in serviziSelected:
            if servizio not in listaPossibili:
                check = False
                break
        self.assertFalse(check)

    def testServiceCameraFound(self):
        p1 = User.objects.create(username="prova3", email="prova3", password="prova1")
        h1 = Hotel.objects.create(nome="La Stella", descrizione="La Stella",
                                  citta="Roma", indirizzo="Via Roma 1", proprietario=p1)
        c1 = Camera(hotel=h1, numero=8, posti_letto=5, servizi="Climatizzatore, Wifi")

        listaPossibili = ["Climatizzatore", "Wifi", "Tv", "Minifrigo"]
        check = False
        serviziSelected = []
        serviziSelected = c1.servizi.split(", ")
        print(serviziSelected)
        for servizio in serviziSelected:
            if servizio in listaPossibili:
                check = True
            else:
                check = False
                print(servizio)
                break

        self.assertTrue(check)

class ViewsTest(TestCase):

    #controlla che l'index restituisca una risposta (se la risposta è 200)
    def testIndexStatusCode(self):
        response = self.client.get(reverse("booking:index"))
        self.assertEqual(response.status_code, 200)

    # controlla che la pagina login restituisca una risposta (se la risposta è 200)
    def testLoginStatusCode(self):
        response = self.client.get(reverse("booking:login"))
        self.assertEqual(response.status_code, 200)

    # controlla che la home restituisca una risposta (se la risposta è 200)
    def testHomeStatusCodeWithoutLogin(self):
        response = self.client.get(reverse("booking:home"))
        #la home non può essere acceduta senza il login
        self.assertNotEqual(response.status_code, 200)

    def testHotelsStatusCodeWithoutLogin(self):
        response = self.client.get(reverse("booking:hotels"))
        self.assertNotEqual(response.status_code, 200)

    def testHotelDetailsStatusCodeWithoutLogin(self):
        u1 = User.objects.create_user(username="prova@prova.com", email="prova@prova.com", password="prova")
        h1 = Hotel.objects.create(proprietario=u1, nome="Stella", descrizione="bello",
                                  citta="Roma", indirizzo="Via Milano 2")

        response = self.client.get("/hoteldetail/<str:hotel>", {"hotel": h1})
        self.assertNotEqual(response.status_code, 200)



    def testHomeWithLogin(self):
        user = User.objects.create(username="prova@gmail.com", email="prova@gmail.com", password="prova")
        self.client.force_login(user)
        response = self.client.get(reverse("booking:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logout")

    def testViewHotels(self):
        u1 = User.objects.create_user(username="prova@gmail.com", email="prova@gmail.com", password="prova")
        h1 = Hotel.objects.create(nome="Stella", descrizione="Bella", citta="Roma",
                                  indirizzo="Via Milano 2", proprietario=u1)
        self.client.force_login(u1)
        response = self.client.get(reverse('booking:hotels'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/hotels.html')
        self.assertContains(response, "Stella")


    def testAddHotel(self):
        u1 = User.objects.create_user(username="prova@gmail.com", email="prova@gmail.com", password="prova")
        self.client.force_login(u1)
        response = self.client.post(reverse('booking:hotels'), {'nome': 'Stella', 'descrizione': 'Bella',
                                                                'citta': 'Roma', 'indirizzo': 'Via Milano 2'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/hotels.html')
        self.assertContains(response, "Stella")
        self.assertEqual(len(Hotel.objects.all()), 1)


    def testAddWrongHotel(self):
        u1 = User.objects.create_user(username="prova@gmail.com", email="prova@gmail.com", password="prova")
        h1 = Hotel.objects.create(nome="Stella", descrizione="Bella", citta="Roma",
                                  indirizzo="Via Milano 2", proprietario=u1)
        self.client.force_login(u1)
        response = self.client.post(reverse('booking:hotels'), {'nome': 'Stella', 'descrizione': 'Bella',
                                                                'citta': 'Roma', 'indirizzo': 'Via Milano 2'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/hotels.html')
        self.assertContains(response, "Non ci possono essere due hotel con nome uguale")
        self.assertEqual(len(Hotel.objects.all()), 1)

    def testViewCameras(self):
        u1 = User.objects.create_user(username="prova@gmail.com", email="prova@gmail.com", password="prova")
        h1 = Hotel.objects.create(nome="Stella", descrizione="Bella", citta="Roma",
                                  indirizzo="Via Milano 2", proprietario=u1)
        c1 = Camera.objects.create(hotel=h1, numero=10, posti_letto=10, servizi="Climatizzatore")
        self.client.force_login(u1)
        response = self.client.get(reverse('booking:hoteldetail', kwargs={'hotel': h1.nome}))
        self.assertTemplateUsed(response, 'booking/hoteldetail.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Stella")
        self.assertContains(response, "Climatizzatore")

    def testAddCamera(self):
        u1 = User.objects.create_user(username="prova@gmail.com", email="prova@gmail.com", password="prova")
        h1 = Hotel.objects.create(nome="Stella", descrizione="Bella", citta="Roma",
                                  indirizzo="Via Milano 2", proprietario=u1)
        self.client.force_login(u1)
        response = self.client.post(reverse('booking:hoteldetail', kwargs={'hotel': h1.nome}),
                                    {'posti_letto': 10, 'numero': 20, 'servizi': 'Climatizzatore'})
        self.assertTemplateUsed(response, 'booking/hoteldetail.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Stella")
        self.assertContains(response, "Climatizzatore")
        self.assertEqual(len(Camera.objects.all()), 1)
    def testAddWrongCamera(self):
        u1 = User.objects.create_user(username="prova@gmail.com", email="prova@gmail.com", password="prova")
        h1 = Hotel.objects.create(nome="Stella", descrizione="Bella", citta="Roma",
                                  indirizzo="Via Milano 2", proprietario=u1)
        c1 = Camera.objects.create(hotel=h1, numero=10, posti_letto=10, servizi="Climatizzatore")
        self.client.force_login(u1)
        response = self.client.post(reverse('booking:hoteldetail', kwargs={'hotel': h1.nome}),
                                    {'posti_letto': 10, 'numero': 10, 'servizi': 'Climatizzatore'})
        self.assertTemplateUsed(response, 'booking/hoteldetail.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Stella")
        self.assertEqual(len(Camera.objects.all()), 1)
        self.assertContains(response, "Non ci possono essere due camere con lo stesso numero")

    def testAddWrongServiziCamera(self):
        u1 = User.objects.create_user(username="prova@gmail.com", email="prova@gmail.com", password="prova")
        h1 = Hotel.objects.create(nome="Stella", descrizione="Bella", citta="Roma",
                                  indirizzo="Via Milano 2", proprietario=u1)
        self.client.force_login(u1)
        response = self.client.post(reverse('booking:hoteldetail', kwargs={'hotel': h1.nome}), {'posti_letto': 10, 'numero': 10, 'servizi': 'Nulla'})
        self.assertTemplateUsed(response, 'booking/hoteldetail.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Stella")
        self.assertEqual(len(Camera.objects.all()), 0)
        self.assertContains(response, "Hai inserito dei servizi errati")


class UserTest(unittest.TestCase):

    def testInitialize(self):
        self.assertEqual(len(Camera.objects.all()), 0)
        self.assertEqual(len(Hotel.objects.all()), 0)
        self.assertEqual(len(Prenotazione.objects.all()), 0)

#Test che testa se creando un utente e aggiungendolo al database, la lista degli utenti si incrementa di 1
    def testAddUserDB(self):
        # test assert classi
        self.user = User.objects.create_user(username='test@test.com', password='!')
        self.assertEqual(len(User.objects.all()), 1)

#Test per verificare un utente creato si effettivamente di tipo utente
    def testIsUser(self):
        self.user = User(username='test@test.com', password='!')
        self.assertIsInstance(self.user, User)

#Test che controlla se i due utenti creati non sono uguali
    def testIsAlreadyPresent(self):
        user2 = User(username='test@test.com', password='!')
        username = User.objects.get(username=user2.username)
        self.assertEqual(username.username,user2.username)


    #Test che controlla se l'utente fa il login correttamente
    def testLogin(self):
        self.client = Client()
        self.username = 'test2@test.com'
        self.email = 'test2@test.com'
        self.password = 'test2'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)
        self.test_user.save()
        login = self.client.login(username=self.username, email=self.email, password=self.password)
        self.assertEqual(login, True)

    # Test che controlla che il proprietario dell'hotel sia effettivamente l'utente creato
    def testAssignHotel(self):
        self.user = User(username='test@test.com', email='test@test.com', password='!')
        self.hotel = Hotel(nome="testHotel", descrizione="molto famoso", citta="Cagliari",
                           indirizzo="via campo pisano 34", proprietario=self.user)
        self.assertEqual(self.hotel.proprietario, self.user)


        # self.assertIsInstance(self.hotel, Hotel)

    # controlla se l'username di un utente viene cambiata correttamente
    def testChangeUsernamelUser(self):
        self.user = User(username='test@test.com', password='!')
        oldUsername = self.user.username
        self.user.username = "cambio@username.com"
        self.assertNotEqual(self.user.username, oldUsername)

    #Test che controlla se la mail inserita ha il formato corretto
    def testCorrectEmailInput(self):
        self.user = User(username='test@test.com', email='test@test.com',password='!')
        self.assertEqual(1, self.user.email.count('@'))


    # controlla se la password di un utente viene cambiata correttamente
    def testChangePasswordUser(self):
        self.user = User(username='test@test.com', password='!')
        oldPsw = self.user.password
        self.user.password = "newPassword"
        self.assertNotEqual(self.user.password, oldPsw)

    # controlla se l'email di un utente viene cambiata correttamente
    def testChangeEmailUser(self):
        self.user = User(email='test@test.com', password='!')
        oldEmail = self.user.email
        self.user.email = "new@Email.com"
        self.assertNotEqual(self.user.email, oldEmail)


class PrenotazioneTest(TestCase):

    def createPrenotazione(self):
        u1 = User.objects.create(username="prova1@gmail.com", email="prova1@gmail.com", password="prova1")
        h1 = Hotel.objects.create(nome="La Stella", descrizione="La Stella",citta="Roma", indirizzo="Via Roma 1", proprietario=u1)
        c1 = Camera.objects.create(hotel=h1, numero=1, posti_letto=5, servizi="Condizionatore")
        p1 = Prenotazione.objects.create(email="email1@gmail.com", camera = c1, checkin = "2018-01-20", checkout = "2018-01-21")
        return p1

    def testCreatePrenotazione(self):
        self.assertTrue(self.createPrenotazione())

    # controlla se viene creato la camera
    def testPrenotazioneInstance(self):
        p1 = self.createPrenotazione()
        self.assertIsInstance(p1, Prenotazione)

    def testDataPrenotazione(self):
        p1 = self.createPrenotazione()
        self.assertLessEqual(p1.checkin, p1.checkout)

    def testInsertEmail(self):
        p1 = self.createPrenotazione()
        self.assertEqual(1, p1.email.count('@'))

    def testPrenotazioneCameraInstance(self):
        p1 = self.createPrenotazione()
        self.assertIsInstance(p1.camera, Camera)

    def testAddPrenotazioneDB(self):
        p1 = self.createPrenotazione()
        self.assertEqual(len(Prenotazione.objects.all()), 1)

    def testPrenotazioneCameraExist(self):
        p1 = self.createPrenotazione()
        for pren in Prenotazione.objects.all():
            self.assertEqual(p1.camera, pren.camera)

#L’albergatore, dopo aver effettuato l’accesso al sistema, visualizza la lista delle prenotazioni qualora ne sia stata fatta qualcuna.

class UserStoriesTest(TestCase):

    def testRegistrazione(self):
        response = self.client.get(reverse('booking:registrazione'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('booking:registraUtente'),
                                    {'email': 'prova@gmail.com', 'password': 'prova', 'nome': 'Mario',
                                     'cognome': 'Rossi'})
        self.assertTemplateUsed(response, 'booking/home.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logout")
        self.assertTrue(response.context['user'].is_authenticated)

    def testLogin(self):
        u1 = User.objects.create_user(username="prova@gmail.com", email="prova@gmail.com", password="prova")
        response = self.client.get(reverse('booking:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/login.html')
        response = self.client.post(reverse('booking:login'), {'email': "prova@gmail.com", 'password': "prova"},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/home.html')
        self.assertContains(response, "Logout")
        self.assertTrue(response.context['user'].is_authenticated)

    def testPrenotazioneCamera(self):
        u1 = User.objects.create_user(username="prova@gmail.com", email="prova@gmail.com", password="prova")
        h1 = Hotel.objects.create(nome="Stella", descrizione="Bello", citta="Roma", indirizzo="Via Milano 2",
                                  proprietario=u1)
        c1 = Camera.objects.create(hotel=h1, numero=2, posti_letto=10, servizi="Condizionatore")
        response = self.client.get(reverse('booking:index'))
        self.assertTemplateUsed(response, 'booking/index.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prenota")
        # Prima il cliente esegue la ricerca
        response = self.client.post(reverse('booking:search'),
                                    {'city': 'Roma', 'size': 4, 'checkin': '2018-01-01', 'checkout': '2018-01-10'})
        self.assertTemplateUsed(response, 'booking/index.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Stella")
        self.assertContains(response, "Condizionatore")
        # Sono comparsi tutti i possibili risultati, l'utente inserisce l'email e completa la prenotazione
        response = self.client.get(reverse('booking:prenota'), {'checkin': '2018-01-01', 'checkout': '2018-01-10',
                                                              'hotel': 'Stella', 'camera': 2,
                                                              'email': 'gianni@gmail.com'})
        self.assertTemplateUsed(response, 'booking/index.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Prenotazione.objects.all()), 1)

    def testVisualizzaPrenotazioni(self):
        self.user = User.objects.create_user(username='proviamo@gmail.com', email='proviamo@gmail.com', password='w')
        response=self.client.post(reverse('booking:login'), { 'email': 'proviamo@gmail.com','password':'w' }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'Logout')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/home.html')

        h1 = Hotel.objects.create(nome="La Stella", descrizione="La Stella", citta="Roma", indirizzo="Via Roma 1",
                                  proprietario=self.user)
        c1 = Camera.objects.create(hotel=h1, numero=1, posti_letto=5, servizi="Climatizzatore")
        p1 = Prenotazione.objects.create(email="email1@gmail.com", camera=c1, checkin="2018-01-20",
                                         checkout="2018-01-21")
        prenotazioni=Prenotazione.objects.all()
        self.assertNotEqual(prenotazioni.count(), 0)
        self.assertTemplateUsed(response, 'booking/home.html')

    def testVisualizzaNessunaPrenotazioni(self):
        self.user = User.objects.create_user(username='proviamo@gmail.com', email='proviamo@gmail.com',
                                             password='w')
        response = self.client.post(reverse('booking:login'), {'email': 'proviamo@gmail.com', 'password': 'w'},
                                    follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'Logout')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/home.html')
        prenotazioni = Prenotazione.objects.all()
        self.assertEqual(prenotazioni.count(), 0)
        self.assertTemplateUsed(response, 'booking/home.html')

    def testGestioneCatenaHotel(self):
        print(Hotel.objects.all())
        self.user = User.objects.create_user(username='proviamo@gmail.com', email='proviamo@gmail.com',
                                             password='w')
        response = self.client.post(reverse('booking:login'), {'email': 'proviamo@gmail.com', 'password': 'w'},
                                    follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'Logout')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/home.html')

        response2 = self.client.get(reverse('booking:hotels'), follow=True)
        self.assertTrue(response2.context['user'].is_authenticated)
        self.assertContains(response2, 'Numero Camere')
        self.assertEquals(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'booking/hotels.html')

        response3 = self.client.post(reverse('booking:hotels'),
                                     {'nome': 'Gigi', 'descrizione': 'La Piovra', 'citta': 'Napoli',
                                      'indirizzo': 'Via Napoli 1'}, follow=True)
        self.assertEquals(response3.status_code, 200)
        self.assertContains(response3, 'Lista Hotels')
        self.assertTemplateUsed(response3, 'booking/hotels.html')

#L’albergatore dopo aver selezionato un hotel, può visualizzare le informazioni ad esso relative e la lista delle camere presenti.
# L’albergatore può aggiungere a questo punto una nuova camera inserendo il relativo numero, i posti letto e i servizi.

    def testGestioneHotel(self):
        print(Hotel.objects.all())
        self.user = User.objects.create_user(username='proviamo@gmail.com', email='proviamo@gmail.com',
                                             password='w')
        response = self.client.post(reverse('booking:login'), {'email': 'proviamo@gmail.com', 'password': 'w'},
                                    follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'Logout')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/home.html')

        response2 = self.client.get(reverse('booking:hotels'), follow=True)
        self.assertTrue(response2.context['user'].is_authenticated)
        self.assertContains(response2, 'Numero Camere')
        self.assertEquals(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'booking/hotels.html')

        h1 = Hotel.objects.create(nome="La Stella", descrizione="La Stella", citta="Roma", indirizzo="Via Roma 1",
                                  proprietario=self.user)

        response3 = self.client.get(reverse('booking:hoteldetail', kwargs={'hotel': Hotel.objects.get(id=1)}), follow=True)
        self.assertContains(response3, 'Descrizione')
        self.assertEquals(response3.status_code, 200)
        self.assertTemplateUsed(response3, 'booking/hoteldetail.html')

        response4 = self.client.get(reverse('booking:hoteldetail', kwargs={'hotel': Hotel.objects.get(id=1)}), {'posti_letto': 5,'numero':1,'servizi':'Tv'}, follow=True)
        self.assertEquals(response4.status_code, 200)
        self.assertTemplateUsed(response4, 'booking/hoteldetail.html')
        self.assertContains(response4, 'Logout')


if __name__ == '__main__':
      unittest.main()





