from Data.repository import Repo
from Data.models import *
from typing import List


# V tej datoteki bomo definirali razred za obdelavo in delo s transakcijami

class ParkirisceService:
    def __init__(self) -> None:
        # Potrebovali bomo instanco repozitorija. Po drugi strani bi tako instanco 
        # lahko dobili tudi kot input v konstrukturju.
        self.repo = Repo()

    def parkirisce(self) -> List[Parkirisce]:
        return self.repo.dobi_parkirisca()
    
    def dobi_oseboDto(self) -> List[Oseba]:               
        osebe = [Oseba.from_dict(t) for t in self.cur.fetchall()]
        return osebe

        