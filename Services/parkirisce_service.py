from Data.repository import Repo
from Data.models import *
from typing import List
import sqlite3
from datetime import datetime

# V tej datoteki bomo definirali razred za obdelavo in delo s transakcijami

class ParkirisceService:
    def __init__(self) -> None:
        # Potrebovali bomo instanco repozitorija. Po drugi strani bi tako instanco 
        # lahko dobili tudi kot input v konstrukturju.
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
        # Preveri, če oseba obstaja (uporabniško ime je edinstveno)
        return self.repo.obstaja_oseba(uporabnisko_ime)

        
    def dobi_zasedena_mesta(self,lokacija: str) -> List[int]:
            return self.repo.dobi_zasedena_mesta(lokacija)

    def dodaj_osebo(self, uporabnisko_ime, ime, priimek, telefonska_stevilka, geslo):
        self.repo.dodaj_osebo(uporabnisko_ime, ime, priimek, telefonska_stevilka, geslo)

 
  

   


        

