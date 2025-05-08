import csv
from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
import os

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

# Funkcija za branje podatkov o parkiriščih iz CSV datoteke
def preberi_parkirisca():
    parkirisca = []
    try:
        with open('parkirisca.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Pretvorimo podatke v ustrezen format (npr. številke za prostih mest)
                parkirisce = {
                    "naziv": row["Parkirišče"],
                    "dnevni_prosta": row["Dnevni prosta"],
                    "dnevni_na_voljo": row["Dnevni na voljo"],
                    "abonenti_na_voljo": row["Abonenti na voljo"],
                    "abonenti_oddana": row["Abonenti oddana"],
                    "abonenti_prosta": row["Abonenti prosta"]
                }
                parkirisca.append(parkirisce)
    except FileNotFoundError:
        pass  # Če datoteka ne obstaja, jo lahko ignoriramo
    return parkirisca

# Funkcija za zaščito dostopa, ki zahteva prijavo
def cookie_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        cookie = request.get_cookie("uporabnik")
        if cookie:
            return f(*args, **kwargs)
        return template("prijava.html", uporabnik=None, rola=None, napaka="Potrebna je prijava!")
    return decorated

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')

@get('/')
@cookie_required
def index():
    parkirisca = preberi_parkirisca()  # Preberemo parkirišča iz CSV-ja
    return template_user('parkirisca.html', parkirisca=parkirisca)

@get('/dodaj_parkirisce')
@cookie_required
def dodaj_parkirisce():
    return template_user('dodaj_parkirisce.html')

@post('/dodaj_parkirisce')
@cookie_required
def dodaj_parkirisce_post():
    lokacija = request.forms.get('lokacija')
    st_mest = int(request.forms.get('st_prostih_mest'))
    # Tukaj lahko dodaš kodo za dodajanje parkirišča v CSV (če je potrebno)
    redirect(url('/'))

@get('/uredi_parkirisce/<id:int>')
@cookie_required
def uredi_parkirisce(id):
    parkirisca = preberi_parkirisca()
    if id < 0 or id >= len(parkirisca):
        return "Parkirišče ni najdeno."
    parkirisce = parkirisca[id]
    return template_user('uredi_parkirisce.html', parkirisce=parkirisce)

@get('/odjava')
def odjava():
    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
    return template('prijava.html', uporabnik=None, rola=None, napaka=None)

if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
