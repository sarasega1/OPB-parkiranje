from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
from Services.auth_service import AuthService
from Services.parkirisce_service import ParkirisceService
#from Services.auth_service import AuthService
import os

# Ustvarimo instance servisov, ki jih potrebujemo. 
# Če je število servisov veliko, potem je service bolj smiselno inicializirati v metodi in na
# začetku datoteke (saj ne rabimo vseh servisov v vseh metodah!)
#python -m venv venv 
# Aktiviramo okolje z venv\Scripts\activate (windows) ali source venv/bin/activate (macos)
# pip install -r requirements.txt 

#SELECT pg_terminate_backend(pid)
#FROM pg_stat_activity
#WHERE wait_event_type = 'Lock'
 # AND query LIKE '%osebe%';
service = ParkirisceService()
auth = AuthService()


# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):                                              # iz requesta dobimo vr. ki pripada ključu - uporabnik. 
        cookie = request.get_cookie("uporabnik")                                  # Če obstaja, mu vrnemo neki, če pa cookie zanj ne obstaja, mu vrne stran za prijavo (torej potrebna je prijava!)
        if cookie:                                                                 # povsod kjer zahtevamo prijavo, bodo s cookie required! 
            return f(*args, **kwargs)
        return template("prijava.html",uporabnik=None, rola=None, napaka="Potrebna je prijava!")
        
    return decorated

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')

def admin_required(f):                # napaka.html? ali pač?
    """
    Dekorator, ki dovoli dostop samo administratorjem.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        rola = request.get_cookie("rola")
        if rola == "admin":
            return f(*args, **kwargs)
        return template("prijava.html", napaka="Dostop zavrnjen. Nimate dovoljenj za dostop do te strani.")
    return decorated




@get('/')
@admin_required
@cookie_required
def index():
    """
    Domača stran z osebami.
    """   
    osebe = service.dobi_oseboDto()
    return template_user('osebe.html', osebe=osebe, stran='osebe')

@get('/')
@cookie_required
def index():
    """
    Domača stran s parkirišči.
    """   
  
    parkirisca = service.dobi_parkirisca()  

        
    return template_user('parkirisca.html', parkirisca = parkirisca) 


@get('/osebe')
@admin_required
@cookie_required
def osebe_view():
    """
    Stran z osebami.
    """   
    osebe = service.dobi_oseboDto()
    print(osebe)
    return template_user('osebe.html', osebe=osebe, stran='osebe')

@post('/registracija')
def registracija_post():
    uporabnisko_ime = request.forms.get('username')
    geslo = request.forms.get('password')
    telefonska_stevilka = request.forms.get('telefonska_stevilka')
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    vloga = 'uporabnik'  # Vedno uporabnik, admin ne sme izbirati!

    # Preverimo, če obstaja uporabnik v bazi uporabnikov
    if auth.obstaja_uporabnik(uporabnisko_ime):
        return template("registracija.html", napaka="Uporabnik že obstaja. Prosim prijavite se.")

    # Preverimo, če obstaja oseba v bazi oseb
    if service.obstaja_oseba(uporabnisko_ime):
        return template("registracija.html", napaka="Uporabniško ime je že zasedeno. Prosim prijavite se.")

    # Preverimo, če so polja prazna
    if not uporabnisko_ime or not geslo or not ime or not priimek:
        return template("registracija.html", napaka="Vsa polja so obvezna.")

    # Dodamo osebo v bazo oseb
    service.dodaj_osebo(
        uporabnisko_ime=uporabnisko_ime,
        ime=ime,
        priimek=priimek,
        telefonska_stevilka=telefonska_stevilka,
        geslo=geslo
    )

    # Dodamo uporabnika v bazo uporabnikov z vlogo 'uporabnik'
    auth.dodaj_uporabnika(uporabnisko_ime, vloga, geslo)

    # Nastavimo piškotke in redirect na domačo stran
    response.set_cookie("uporabnik", uporabnisko_ime)
    response.set_cookie("rola", vloga)
    redirect(url('/'))




@get('/registracija')
def registracija_get():
    rola = request.get_cookie("rola")
    uporabnik = request.get_cookie("uporabnik")
    return template("registracija.html", napaka=None, rola=rola, uporabnik=uporabnik)





@post('/prijava')                                       #glej v views prijava html
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovi roli.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
        return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)
        response.set_cookie("rola", prijava.role)
        
        # redirect v večino primerov izgleda ne deluje
        redirect(url('/'))

        # Uporabimo kar template, kot v sami "index" funkciji

        # transakcije = service.dobi_transakcije()        
        # return template('transakcije.html', transakcije = transakcije)
        
    else:
        return template("prijava.html", uporabnik=None, rola=None, napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")
@get('/prijava')
def prijava_get():
    return template("prijava.html", napaka=None, rola = None)

@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """
    
    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
    
    return template('prijava.html', uporabnik=None, rola=None, napaka=None)




@get('/dobi_parkirisca')
@cookie_required
def parkirisca_view():
    parkirisca = service.dobi_parkirisca()
    rola = request.get_cookie("rola")

    if rola == "admin":
        return template_user('parkirisca.html', parkirisca=parkirisca, stran='parkirisca')
    else:
        return template_user('parkirisca.html', parkirisca=parkirisca, stran='parkirisca')


@get('/parkirisce/<id:int>')
@cookie_required
def podrobnosti_parkirisca(id):
    parkirisce = service.dobi_parkirisce(id)
    if parkirisce is None:
        return template("napaka.html", napaka="Parkirišče ne obstaja.")
    
    rola = request.get_cookie("rola")

    if rola == "admin":
        return template_user("parkirisce_podrobnosti2.html", parkirisce=parkirisce)
    else:
        return template_user("parkirisce_podrobnosti.html", parkirisce=parkirisce)
 # Dokler nimate razvitega vmesnika za dodajanje uporabnikov, jih dodajte kar ročno.
#auth.dodaj_uporabnika('gasper', 'admin', 'gasper')




@get('/rezervacija/<mesto_id:int>/<lokacija>')
def prikazi_rezervacijo(mesto_id, lokacija):
    s = request.environ.get('beaker.session')
    if s:
        uporabnik = {
            'ime': s.get('ime'),
            'priimek': s.get('priimek'),
            'uporabnisko_ime': s.get('uporabnisko_ime'),
            'rola': s.get('rola')
        } if s.get('ime') else None
    else:
        uporabnik = None

    rola = uporabnik['rola'] if uporabnik else None

    # Dodaj prazne vrednosti za formo
    return template_user('rezervacija.html',
                         napaka=None,
                         mesto_id=mesto_id,
                         lokacija = lokacija,
                         registrska_stevilka='',
                         prihod='',
                         odhod='')








@post('/rezervacija/<mesto_id:int>')
@cookie_required
def rezervacija_post(mesto_id):
    uporabnisko_ime = request.get_cookie("uporabnik")
    if not uporabnisko_ime:
        return redirect(url('/prijava'))

    # Preberi podatke iz obrazca, vključno z lokacijo
    registrska_stevilka = request.forms.get('registrska_stevilka')
    prihod = request.forms.get('prihod')
    odhod = request.forms.get('odhod')
    lokacija = request.forms.get('lokacija')   # pomembno!

    if not prihod or not odhod:
        return template_user('rezervacija.html', mesto_id=mesto_id, lokacija=lokacija, napaka="Prihod ali odhod nista vnešena.",
                             registrska_stevilka=registrska_stevilka, prihod=prihod, odhod=odhod)

    try:
        service.naredi_rezervacijo(lokacija, mesto_id, uporabnisko_ime, registrska_stevilka, prihod, odhod)
    except ValueError as e:
        return template_user('rezervacija.html', mesto_id=mesto_id, lokacija=lokacija, napaka=str(e),
                             registrska_stevilka=registrska_stevilka, prihod=prihod, odhod=odhod)

    return template_user("rezervacija_uspesna.html", sporocilo="Rezervacija uspešna!")




@get('/rezervacije')
@admin_required
@cookie_required
def vse_rezervacije():
    rezervacije = service.dobi_rezervacije()
    return template_user('rezervacije.html', rezervacije=rezervacije, napaka = None, stran = 'rezervacije')



if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True) 