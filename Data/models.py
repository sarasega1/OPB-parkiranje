from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime, time



@dataclass_json
@dataclass
class Oseba:
    uporabnisko_ime : str = field(default="")  
    geslo : str = field(default="")
    telefonska_stevilka : int = field(default=0)
    ime: str = field(default="")
    priimek: str = field(default="")
    


@dataclass_json
@dataclass
class Parkirisce:
    id : int = field(default=0)
    lokacija : str = field(default="") 
    dnevni_na_voljo: int = field(default=0)




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

def convert_to_datetime(value):
    if isinstance(value, time):
        return datetime.combine(datetime.today(), value)
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except:
            pass
    return value
@dataclass_json
@dataclass
class Rezervacija:
    id_parkirnega_mesta: int = field(default=0)
    lokacija: str = field(default="")
    prihod: datetime = field(default_factory=datetime.now, metadata=config(decoder=convert_to_datetime))
    odhod: datetime = field(default_factory=datetime.now, metadata=config(decoder=convert_to_datetime))
    uporabnisko_ime: str = field(default="")
    registrska_stevilka: str = field(default="")

    @staticmethod
    def from_dict(d: dict) -> "Rezervacija":
        def convert_to_datetime(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, time):
                return datetime.combine(datetime.today(), value)
            if isinstance(value, str):
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M"):
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
                print(f"⚠️ Neznan format datuma: {value}")
            return value

        return Rezervacija(
            id_parkirnega_mesta=d.get("id_parkirnega_mesta", 0),
            lokacija=d.get("lokacija", ""),
            prihod=convert_to_datetime(d.get("prihod")),
            odhod=convert_to_datetime(d.get("odhod")),
            uporabnisko_ime=d.get("uporabnisko_ime", ""),
            registrska_stevilka=d.get("registrska_stevilka", ""),
        )

    @classmethod
    def from_row(cls, row):
        return cls.from_dict(dict(row))