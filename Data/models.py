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


from datetime import datetime, time

@dataclass_json
@dataclass
class Rezervacija:
    id_parkirnega_mesta: int = field(default=0)
    lokacija: str = field(default="")
    prihod: datetime = field(default_factory=datetime.now)
    odhod: datetime = field(default_factory=datetime.now)
    uporabnisko_ime: str = field(default="")
    registrska_stevilka: str = field(default="")

    @staticmethod
    def from_dict(d: dict) -> "Rezervacija":
        # Pretvori čas v datetime, če je potrebno
        def convert_to_datetime(value):
            if isinstance(value, time):
                # Ker nimamo datuma, dodamo današnji datum ali nek fiksni datum
                return datetime.combine(datetime.today(), value)
            if isinstance(value, str):
                # Poskusi parse datetime string
                try:
                    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                except:
                    pass
            return value

        return Rezervacija(
            id_parkirnega_mesta=d.get("id_parkirnega_mesta", 0),
            lokacija=d.get("lokacija", ""),
            prihod=convert_to_datetime(d.get("prihod")),
            odhod=convert_to_datetime(d.get("odhod")),
            uporabnisko_ime=d.get("uporabnisko_ime", ""),
            registrska_stevilka=d.get("registrska_stevilka", ""),
        )
