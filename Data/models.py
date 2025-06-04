from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime



@dataclass_json
@dataclass
class Oseba:
    uporabnisko_ime : str = field(default="")  # Za vsako polje povemo tip in privzeto vrednost
    geslo : str = field(default="")
    telefonska_stevilka : int = field(default=0)
    registrska_stevilka : str = field(default="")
    trr : str = field(default="")
    ime: str = field(default="")
    priimek: str = field(default="")
    #emso: int = field(default=0)


@dataclass_json
@dataclass
class Racun:    
    id_placila : int = field(default=0)
    znesek : int = field(default=0)



@dataclass_json
@dataclass
class Parkirisce:
    id : int = field(default=0)
    lokacija : str = field(default="") 
    dnevni_na_voljo: int = field(default=0)
    dnevni_zasedeni: int = field(default=0)
    
    @property
    def zasedenost(self) -> str:
        # Prikaz zasedenosti v formatu "prosta/na_voljo"
        return f"{self.dnevni_zasedeni}/{self.dnevni_na_voljo}"
    #Se bo to dalo?

    


@dataclass_json
@dataclass
class ParkirisceDto:
    id : int = field(default=0)
    st_prostih_mest : int = field(default=0)
    lokacija : str = field(default="") 
    trr:  str = field(default="") 


@dataclass_json
@dataclass
class Parkirno_mesto:
    id_parkirnega_mesta : int = field(default=0)
    lokacija_parkirnega_mesta : str = field(default="") 
    status : str = field(default="")


@dataclass_json
@dataclass

class Zgodovina:
    cas_prihoda : str = field(default="") 
    cas_odhoda : str = field(default="") 
    
@dataclass_json
@dataclass
class Uporabnik:
    username: str = field(default="")
    role: str = field(default="")
    password_hash: str = field(default="")
    last_login: str = field(default="")

@dataclass
class UporabnikDto:
    username: str = field(default="")
    role: str = field(default="") 


@dataclass_json
@dataclass
class Rezervacija:
    id_parkirnega_mesta: int = field(default=0)
    lokacija: str = field(default="")
    prihod: datetime
    odhod: datetime
    uporabnisko_ime: str = field(default="")    