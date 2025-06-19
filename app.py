from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
from Services.auth_service import AuthService
from Services.parkirisce_service import ParkirisceService
#from Services.auth_service import AuthService
import os

# Ustvarimo instance servisov, ki jih potrebujemo. 
# Če je število servisov veliko, potem je service bolj smiselno inicializirati v metodi in na
# začetku datoteke (saj ne rabimo vseh servisov v vseh metodah!)

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
    return template("prijava.html", napaka=None)

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



@post('/rezervacija/<mesto_id:int>')
def rezervacija_post(mesto_id):
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    registracija = request.forms.get('registracija')
    prihod = request.forms.get('prihod')
    odhod = request.forms.get('odh')

    service.naredi_rezervacijo(mesto_id, ime, priimek, registracija, prihod, odhod)
    return redirect(url('/parkirisce/1'))


@get('/rezervacija/<mesto_id:int>')
def prikazi_rezervacijo(mesto_id):
    # pridobi uporabnikovo vlogo iz seje ali druge logike
    rola = 'admin'  # ali 'uporabnik', ali None
    uporabnik = None 
    return template('rezervacija.html', mesto_id=mesto_id, rola=rola, uporabnik=uporabnik)


if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)




