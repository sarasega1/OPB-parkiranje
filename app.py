from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
from Services.auth_service import AuthService
from Services.parkirisce_service import ParkirisceService
import os
from datetime import datetime

#python -m venv venv 
# Aktiviramo okolje z venv\Scripts\activate (windows) ali source venv/bin/activate (macos)
# pip install -r requirements.txt 

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
    def decorated( *args, **kwargs):                                            
        cookie = request.get_cookie("uporabnik")                                
        if cookie:                                                                 
            return f(*args, **kwargs)
        return template("prijava.html",uporabnik=None, rola=None, napaka="Potrebna je prijava!")
        
    return decorated

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')

def admin_required(f):                
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
    vloga = 'uporabnik'  

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



@post('/prijava')                                      
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
       
        redirect(url('/'))
        
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
    zasedena_mesta = service.dobi_zasedena_mesta(parkirisce.lokacija)
    vsa_mesta = list(range(1, parkirisce.dnevni_na_voljo + 1))
    mesta_status = [(i, i in zasedena_mesta) for i in vsa_mesta]
    mesta_status.sort(key=lambda x: x[1])  
    if rola == "admin":
        return template_user("parkirisce_podrobnosti2.html", parkirisce=parkirisce, mesta_status=mesta_status, zasedena_mesta = zasedena_mesta)
    else:
        return template_user("parkirisce_podrobnosti.html", parkirisce=parkirisce, mesta_status=mesta_status, zasedena_mesta= zasedena_mesta)





@get('/rezervacija/<mesto_id:int>/<lokacija>')
@cookie_required
def prikazi_rezervacijo(mesto_id, lokacija):
    now = datetime.now()
    min_datetime = now.strftime("%Y-%m-%dT%H:%M")
    max_datetime = now.replace(hour=23, minute=59, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M")
    
    return template_user('rezervacija.html',
                         napaka=None,
                         mesto_id=mesto_id,
                         lokacija=lokacija,
                         registrska_stevilka='',
                         prihod=min_datetime,
                         odhod='',
                         min_datetime=min_datetime,
                         max_datetime=max_datetime)




@post('/rezervacija/<mesto_id:int>')
@cookie_required
def rezervacija_post(mesto_id):
    uporabnisko_ime = request.get_cookie("uporabnik")
    if not uporabnisko_ime:
        return redirect(url('/prijava'))

    registrska_stevilka = request.forms.get('registrska_stevilka')
    prihod = request.forms.get('prihod')
    odhod = request.forms.get('odhod')
    lokacija = request.forms.get('lokacija')

    now = datetime.now()
    min_datetime = now.strftime("%Y-%m-%dT%H:%M")
    max_datetime = now.replace(hour=23, minute=59, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M")

    if not prihod or not odhod:
        return template_user('rezervacija.html',
                             mesto_id=mesto_id,
                             lokacija=lokacija,
                             napaka="Prihod ali odhod nista vnešena.",
                             registrska_stevilka=registrska_stevilka,
                             prihod=prihod,
                             odhod=odhod,
                             min_datetime=min_datetime,
                             max_datetime=max_datetime)

    try:
        service.naredi_rezervacijo(lokacija, mesto_id, uporabnisko_ime, registrska_stevilka, prihod, odhod)
    except ValueError as e:
        return template_user('rezervacija.html',
                             mesto_id=mesto_id,
                             lokacija=lokacija,
                             napaka=str(e),
                             registrska_stevilka=registrska_stevilka,
                             prihod=prihod,
                             odhod=odhod,
                             min_datetime=min_datetime,
                             max_datetime=max_datetime)

    return template_user("rezervacija_uspesna.html", sporocilo="Rezervacija uspešna!")



@get('/rezervacije')
@admin_required
@cookie_required
def vse_rezervacije():
    rezervacije = service.dobi_rezervacije()
    return template_user('rezervacije.html', moje_rezervacije=rezervacije, napaka = None, stran = 'rezervacije')



@get('/moje_rezervacije')
@cookie_required
def moje_rezervacije():
    uporabnisko_ime = request.get_cookie("uporabnik")
    if uporabnisko_ime is None:
        redirect('/prijava')

    service = ParkirisceService()
    rezervacije = service.dobi_rezervacije_uporabnika(uporabnisko_ime)
    uporabnik = service.dobi_uporabnika(uporabnisko_ime)
    now = datetime.now()
    # lahko filtriraš aktivne že tukaj
    aktivne_rezervacije = [r for r in rezervacije if r.prihod <= now <= r.odhod]

    return template('moje_rezervacije', moje_rezervacije=rezervacije, aktivne_rezervacije=aktivne_rezervacije, now=now)
from bottle import post, request, redirect




@get('/preklici_rezervacijo/<lokacija>/<id_parkirnega_mesta:int>')
@cookie_required
def potrdi_preklic(lokacija, id_parkirnega_mesta):
    uporabnisko_ime = request.get_cookie("uporabnik")
    if not uporabnisko_ime:
        redirect('/prijava')

    service = ParkirisceService()
    rezervacije = service.dobi_rezervacije_uporabnika(uporabnisko_ime)

    # Poišči rezervacijo po lokaciji in ID parkirnega mesta
    rezervacija = next(
        (r for r in rezervacije if r.lokacija == lokacija and r.id_parkirnega_mesta == id_parkirnega_mesta),
        None
    )

    if rezervacija is None:
        return template('napaka.html', napaka="Rezervacija ne obstaja ali nimaš dostopa.")


    sedaj = datetime.now()
    if rezervacija.odhod <= sedaj or rezervacija.prihod.date() != sedaj.date():
        return template('moje_rezervacije', moje_rezervacije=rezervacije, napaka="Preklic ni možen.", now=sedaj)

    

@post('/preklici_rezervacijo/<lokacija>/<id_parkirnega_mesta:int>/potrdi')
@cookie_required
def izvrsi_preklic(lokacija, id_parkirnega_mesta):
    uporabnisko_ime = request.get_cookie("uporabnik")
    if not uporabnisko_ime:
        redirect('/prijava')

    service = ParkirisceService()
    rezervacije = service.dobi_rezervacije_uporabnika(uporabnisko_ime)

    rezervacija = next(
        (r for r in rezervacije if r.lokacija == lokacija and r.id_parkirnega_mesta == id_parkirnega_mesta),
        None
    )

    if rezervacija is None:
        return template('napaka.html', napaka="Rezervacija ne obstaja ali nimaš dostopa.")

    sedaj = datetime.now()
    if rezervacija.odhod <= sedaj or rezervacija.prihod.date() != sedaj.date():
        return template('moje_rezervacije', moje_rezervacije=rezervacije, napaka="Preklic ni možen.", now=sedaj)

    uspeh = service.prekini_rezervacijo(lokacija, id_parkirnega_mesta)

    if uspeh:
        response.set_cookie("flash_message", "Rezervacija je uspesno preklicana.", path="/")

    else:
        response.set_cookie("flash_message", "Preklic rezervacije ni bil uspesen.", path="/")

    redirect('/moje_rezervacije')
@post('/moje_rezervacije')
@cookie_required
def urejanje_rezervacije():
    uporabnisko_ime = request.get_cookie("uporabnisko_ime")
    if uporabnisko_ime is None:
        redirect('/prijava')
    
    service = ParkirisceService()

    lokacija = request.forms.get('lokacija')
    id_parkirnega_mesta = request.forms.get('id_parkirnega_mesta')
    prihod = request.forms.get('prihod')
    akcija = request.forms.get('akcija')

    if not (lokacija and id_parkirnega_mesta and prihod):
        return "Napaka: Manjkajoči podatki."

    if akcija == 'preklici':
        service.odstrani_rezervacijo_po_kljucih(lokacija, id_parkirnega_mesta, prihod)

    elif akcija == 'podaljsaj':
        redirect(f"/podaljsaj_rezervacijo?lokacija={lokacija}&id_parkirnega_mesta={id_parkirnega_mesta}&prihod={prihod}")

    redirect('/moje_rezervacije')

from bottle import request, redirect, template

@get('/podaljsaj_rezervacijo')
@cookie_required
def prikazi_podaljsaj_obrazec():
    uporabnisko_ime = request.get_cookie("uporabnik")
    if uporabnisko_ime is None:
        redirect('/prijava')

    lokacija = request.query.lokacija
    id_parkirnega_mesta = request.query.id_parkirnega_mesta
    prihod = request.query.prihod

    # Prikaži obrazec za izbiro koliko časa želi uporabnik podaljšati
    return template('podaljsaj.html', 
                    lokacija=lokacija, 
                    id_parkirnega_mesta=id_parkirnega_mesta, 
                    prihod=prihod)


from bottle import response

@post('/podaljsaj_rezervacijo')
@cookie_required
def podaljsaj_rezervacijo():
    uporabnisko_ime = request.get_cookie("uporabnik")
    if uporabnisko_ime is None:
        redirect('/prijava')

    lokacija = request.forms.get('lokacija')
    id_parkirnega_mesta = int(request.forms.get('id_parkirnega_mesta'))
    prihod = request.forms.get('prihod')
    minute_str = request.forms.get('cas')
    if minute_str is None:
        response.status = 400
        return "Napaka: Manjka podatek 'cas'"

    minute = int(minute_str)

    from datetime import datetime
    prihod_dt = datetime.strptime(prihod, "%Y-%m-%d %H:%M:%S")

    service = ParkirisceService()
    rezervacija = service.repo.dobi_rezervacijo_po_kljucih(lokacija, id_parkirnega_mesta, prihod_dt)
    if rezervacija is None:
        return "Rezervacija je potekla ali ne obstaja."

    # če obstaja, nadaljuj s podaljšanjem
    service.podaljsaj_rezervacijo_po_kljucih(lokacija, id_parkirnega_mesta, prihod_dt, minute)

    redirect('/moje_rezervacije')


# Spremeni formo v 'moje_rezervacije.html':
# Namesto POST na /moje_rezervacije, naj gumb "Prekliči" vodi na /preklici_rezervacijo/{{r.id}}

# npr.
# <td><a href="/preklici_rezervacijo/{{r.id}}">Prekliči</a></td>



if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)

