from Data.repository import Repo
from Data.models import *
from typing import List
from datetime import datetime, timedelta



class ParkirisceService:
    def __init__(self) -> None:
        self.repo = Repo()

    def parkirisca(self) -> List[Parkirisce]:
        return self.repo.dobi_parkirisca()
    
    def dobi_oseboDto(self) -> List[Oseba]:
        return self.repo.dobi_oseboDto()

    
    def dobi_parkirisca(self) -> List[Parkirisce]:               
        return self.repo.dobi_parkirisca()
    
    def dobi_parkirisce(self, id: int) -> Parkirisce:
        return self.repo.dobi_parkirisce(id)

    def naredi_rezervacijo(self, lokacija: str,  mesto_id: int, uporabnisko_ime: str, registrska_stevilka: str, prihod_str: str, odhod_str: str) -> None:
        prihod = datetime.strptime(prihod_str, "%Y-%m-%dT%H:%M")
        odhod = datetime.strptime(odhod_str, "%Y-%m-%dT%H:%M")
        sedaj = datetime.now()



        if odhod <= prihod:
            raise ValueError("Odhod mora biti kasneje od prihoda!")

        rezervacija = Rezervacija(
            lokacija = lokacija,
            id_parkirnega_mesta=mesto_id,
            uporabnisko_ime=uporabnisko_ime,
            registrska_stevilka=registrska_stevilka,
            prihod=prihod,
            odhod=odhod
        )
        self.repo.dodaj_rezervacijo(rezervacija)

    def dobi_rezervacije(self):
        return self.repo.dobi_rezervacije()

    def obstaja_oseba(self, uporabnisko_ime: str) -> bool:
    
        return self.repo.obstaja_oseba(uporabnisko_ime)

        
    def dobi_zasedena_mesta(self,lokacija: str) -> List[int]:
            return self.repo.dobi_zasedena_mesta(lokacija)

    def dodaj_osebo(self, uporabnisko_ime, ime, priimek, telefonska_stevilka, geslo):
        self.repo.dodaj_osebo(uporabnisko_ime, ime, priimek, telefonska_stevilka, geslo)

    def dobi_uporabnika(self, uporabnisko_ime: str) -> Uporabnik | None:
        return self.repo.dobi_uporabnika(uporabnisko_ime)
    
    def dobi_rezervacije_uporabnika(self, uporabnisko_ime: str) -> List[Rezervacija]:
        return self.repo.dobi_rezervacije_uporabnika(uporabnisko_ime)




    def podaljsaj_rezervacijo_po_kljucih(self, lokacija: str, id_parkirnega_mesta: int, prihod: datetime, minute: int):
        rezervacija = self.repo.dobi_rezervacijo_po_kljucih(lokacija, id_parkirnega_mesta, prihod)
       
        now = datetime.now()

    # če je trenutni odhod v prihodnosti, podaljšaj od njega naprej
        if rezervacija.odhod > now:
            rezervacija.odhod += timedelta(minutes=minute)
        else:
        # če je že potekla, podaljšaj od zdaj naprej
            rezervacija.odhod = now + timedelta(minutes=minute)

        self.repo.posodobi_rezervacijo_po_kljucih(rezervacija)

    def odstrani_rezervacijo_po_kljucih(self, lokacija: str, id_parkirnega_mesta: int, prihod: datetime) -> None:
        self.repo.odstrani_rezervacijo_po_kljucih(lokacija, id_parkirnega_mesta, prihod)

    def prekini_rezervacijo(self, lokacija, id_parkirnega_mesta):
        return self.repo.prekini_rezervacijo(lokacija, id_parkirnega_mesta)
    


        

