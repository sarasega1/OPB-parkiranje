from Data.repository import Repo
from Data.models import *
from typing import List

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

   
    def dobi_rezervacije(self) -> List[Rezervacija]:               
        return self.repo.dobi_rezervacije()


def naredi_rezervacijo(self, mesto_id: int, ime: str, priimek: str, registracija: str, prihod: str, odhod: str) -> None:
    prihod_dt = datetime.strptime(prihod, "%Y-%m-%dT%H:%M")
    odhod_dt = datetime.strptime(odhod, "%Y-%m-%dT%H:%M")
def naredi_rezervacijo(self, mesto_id: int, ime: str, priimek: str, registracija: str, prihod: str, odhod: str) -> None:
    rezervacija = Rezervacija(
        id_parkirnega_mesta=mesto_id,
        ime=ime,
        priimek=priimek,
        registracija=registracija,
        prihod=prihod,
        odhod=odhod
    )
    self.repo.dodaj_rezervacijo(rezervacija)


    # Vrne vsa parkirna mesta za določeno parkirišče
    def dobi_parkirna_mesta(self, parkirisce_id: int) -> List[Parkirno_mesto]:
        return self.repo.dobi_parkirna_mesta(parkirisce_id)

"""  def dobi_oseboDto(self) -> List[Oseba]:               
        osebe = [Oseba.from_dict(t) for t in self.cur.fetchall()]
        return osebe
"""

   


        
