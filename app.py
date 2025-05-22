from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.parkirisce_service import ParkirisceService
#from Services.auth_service import AuthService
import os

# Ustvarimo instance servisov, ki jih potrebujemo. 
# Če je število servisov veliko, potem je service bolj smiselno inicializirati v metodi in na
# začetku datoteke (saj ne rabimo vseh servisov v vseh metodah!)

service = ParkirisceService()
#auth = AuthService()


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


@get('/')
@cookie_required
def index():
    """
    Domača stran s osebami.
    """   
  

    transakcije_dto = service.dobi_transakcije_dto()  

        
    return template_user('osebe.html', osebe = transakcije_dto)

@get('/osebe')

def index():
    """
    Domača stran z osebami.    """   
  
    osebe = service.dobi_oseboDto()
    return template_user('osebe.html', osebe = osebe)




@get('/transakcije_dto')
def transakcije_dto():
    """
    Stran z dto transakcijami.
    """   
  
    transakcije_dto = service.dobi_transakcije_dto()  
        
    return template_user('transakcije_dto.html', transakcije = transakcije_dto)

@get('/dodaj_transakcijo')
def dodaj_transakcijo():
    """
    Stran za dodajanje transakcije.  """
    osebe = service.dobi_osebe_dto()    
    return template_user('dodaj_transakcijo.html', osebe=osebe)


@post('/dodaj_transakcijo')
def dodaj_transakcijo_post():
    # Preberemo podatke iz forme. Lahko bi uporabili kakšno dodatno metodo iz service objekta

    racun = int(request.forms.get('racun'))
    znesek = float(request.forms.get('znesek'))
    opis = request.forms.get('opis')
    cas = request.forms.get('cas')   

    service.naredi_transakcijo(racun, cas, znesek, opis)
    
    
    redirect(url('/'))

@get('/uredi_transakcijo/<id:int>')
def uredi_transakcijo(id):
    """
    Stran za urejanje transakcije.  """   
    osebe = service.dobi_osebe_dto()  
    transakcija = service.dobi_transakcijo(id)
    return template_user('uredi_transakcijo.html', transakcija =transakcija, osebe = osebe)

@post('/uredi_transakcijo')
def uredi_transakcijo_post():
    """
    Stran za urejanje transakcije.  """ 
    id = int(request.forms.get('id'))  
    racun = int(request.forms.get('racun'))
    znesek = float(request.forms.get('znesek'))
    opis = request.forms.get('opis')   
    cas = request.forms.get('cas') 
    
    service.posodobi_transakcijo(id, racun, cas, znesek, opis)
    redirect(url('/'))

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

@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """
    
    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
    
    return template('prijava.html', uporabnik=None, rola=None, napaka=None)


 # Dokler nimate razvitega vmesnika za dodajanje uporabnikov, jih dodajte kar ročno.
#auth.dodaj_uporabnika('gasper', 'admin', 'gasper')
if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)




