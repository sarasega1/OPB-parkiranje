import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import datetime
import os


from Data.models import Parkirisce, Oseba, ParkirisceDto, Uporabnik, Parkirno_mesto, Rezervacija
from typing import List

# Preberemo port za bazo iz okoljskih spremenljivk
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

## V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.
# py -m Data.repository
class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


    
    def dobi_osebo(self) -> List[Oseba]:               
        self.cur.execute("""
            SELECT ime, priimek, uporabnisko_ime, geslo, telefonska_stevilka, registrska_stevilka, trr
            FROM  osebe
        
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
        osebe = [Oseba.from_dict(t) for t in self.cur.fetchall()]
        return osebe  
    def dobi_oseboDto(self) -> List[Oseba]:               
        self.cur.execute("""
            SELECT ime, priimek, uporabnisko_ime, telefonska_stevilka, registrska_stevilka, trr
            FROM  osebe
        
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
        osebe = [Oseba.from_dict(t) for t in self.cur.fetchall()]
        return osebe


    def dobi_parkirisca(self) -> List[Parkirisce]:               
        self.cur.execute("""
            SELECT id, lokacija, dnevni_zasedeni, dnevni_na_voljo
            FROM parkirisca
        
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
        parkirisca = [Parkirisce.from_dict(t) for t in self.cur.fetchall()]
        return parkirisca
    
    def dobi_parkirisca(self) -> List[Parkirisce]:               
            self.cur.execute("""
                SELECT id, lokacija, dnevni_zasedeni, dnevni_na_voljo
                FROM parkirisca
            
            """)
        
            # rezultate querya pretovrimo v python seznam objektov (transkacij)
            parkirisca = [Parkirisce.from_dict(t) for t in self.cur.fetchall()]
            return parkirisca
    def dobi_parkirisce(self, id: int) -> Parkirisce:
        self.cur.execute("""
                     SELECT id, lokacija, dnevni_zasedeni, dnevni_na_voljo
                     FROM parkirisca
                     WHERE id = %s
                     """, (id,))
        row = self.cur.fetchone()
        if row:
          return Parkirisce.from_dict(row)
        return None
    def obstaja_oseba(self, uporabnisko_ime: str) -> bool:
        self.cur.execute("""
            SELECT COUNT(*) FROM osebe WHERE uporabnisko_ime = %s
        """, (uporabnisko_ime,))
        count = self.cur.fetchone()[0]
        return count > 0

    def dodaj_osebo(self, uporabnisko_ime: str, ime: str, priimek: str, telefonska_stevilka: str, geslo: str) -> None:
        self.cur.execute("""
            INSERT INTO osebe (uporabnisko_ime, ime, priimek, telefonska_stevilka, geslo)
            VALUES (%s, %s, %s, %s, %s)
        """, (uporabnisko_ime, ime, priimek, telefonska_stevilka, geslo))
        self.conn.commit()

    def dobi_rezervacije(self) -> List[Rezervacija]:               
            self.cur.execute("""
                SELECT id, uporabnisko_ime, registrska_stevilka, prihod, odhod
                FROM reuervacija
            
            """)
            
            # rezultate querya pretovrimo v python seznam objektov (transkacij)
            rezervacije = [Rezervacija.from_dict(t) for t in self.cur.fetchall()]
            return rezervacije

    def dodaj_rezervacijo(self, rezervacija: Rezervacija) -> None:
        sql = """
        INSERT INTO rezervacija (id_parkirnega_mesta, ime, priimek, registrska_stevilka, prihod, odhod)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, (
            rezervacija.id_parkirnega_mesta,
            rezervacija.ime,
            rezervacija.priimek,
            rezervacija.registracija,
            rezervacija.prihod,
            rezervacija.odhod
        ))
        self.conn.commit()
        cursor.close()

    def dodaj_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            INSERT into uporabniki(username, role, password_hash, last_login)
            VALUES (%s, %s, %s, %s)
            """, (uporabnik.username,uporabnik.role, uporabnik.password_hash, uporabnik.last_login))
        self.conn.commit()


    def dobi_uporabnika(self, username:str) -> Uporabnik:
        self.cur.execute("""
            SELECT username, role, password_hash, last_login
            FROM uporabniki
            WHERE username = %s
        """, (username,))
         
        u = Uporabnik.from_dict(self.cur.fetchone())
        return u
    
    def posodobi_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            Update uporabniki set last_login = %s where username = %s
            """, (uporabnik.last_login,uporabnik.username))
        self.conn.commit()

    def dodaj_rezervacijo(self, rezervacija):
        try:
            self.cur.execute("""
                INSERT INTO rezervacija (id_parkirnega_mesta, ime, priimek, registracija, prihod, odhod)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (rezervacija.id_parkirnega_mesta, rezervacija.ime, rezervacija.priimek, rezervacija.registracija, rezervacija.prihod, rezervacija.odhod))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e



      


    # def dobi_parkiriscaDto(self) -> List[ParkirisceDto]:               
    #     self.cur.execute("""
    #         SELECT id, lokacija, trr
    #         FROM parkirisca
        
    #     """)
        
    #     # rezultate querya pretovrimo v python seznam objektov (transkacij)
    #     parkirisca = [Parkirisce.from_dict(t) for t in self.cur.fetchall()]
    #     return parkirisca
    

if __name__ == "__main__":
    repo = Repo()
    parkirisca = repo.dobi_parkirisca()

    for p in parkirisca:
        print(p)
if __name__ == "__main__":
    repo = Repo()
    osebe = repo.dobi_osebo()

    for p in osebe:
         print(p)