import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import datetime
import os

from Data.models import Parkirisce, Oseba, ParkirisceDto, Uporabnik
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

  