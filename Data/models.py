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
    trr : int = field(default=0)


@dataclass_json
@dataclass
class Racun:    
    id_placila : int = field(default=0)
    znesek : int = field(default=0)



@dataclass_json
@dataclass
class Parkirisce:
    id_parkirisca : int = field(default=0)
    st_prostih_mest : int = field(default=0)
    lokacija : str = field(default="") 

    


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
    
    