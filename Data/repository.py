import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import os
from datetime import datetime, time
from Data.models import Parkirisce, Oseba, Uporabnik,Rezervacija
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
            SELECT ime, priimek, uporabnisko_ime, telefonska_stevilka
            FROM  osebe
        
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
        osebe = [Oseba.from_dict(t) for t in self.cur.fetchall()]
        return osebe  
    def dobi_oseboDto(self) -> List[Oseba]:               
        self.cur.execute("""
            SELECT ime, priimek, uporabnisko_ime, telefonska_stevilka
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
            INSERT INTO osebe (uporabnisko_ime, ime, priimek, telefonska_stevilka)
            VALUES (%s, %s, %s, %s)
        """, (uporabnisko_ime, ime, priimek, telefonska_stevilka))
        self.conn.commit()

   
    def dobi_rezervacije(self) -> List[Rezervacija]:
        self.cur.execute("SELECT * FROM rezervacija")
        rows = self.cur.fetchall()
        rezervacije = []
        for t in rows:
            prihod = t['prihod']
            odhod = t['odhod']
            # če je čas brez datuma, dodaj datum
            if isinstance(prihod, time):
                prihod = datetime.combine(datetime.today(), prihod)
            if isinstance(odhod, time):
                odhod = datetime.combine(datetime.today(), odhod)

            r = Rezervacija(  
                id_parkirnega_mesta=t['id_parkirnega_mesta'],
                lokacija=t.get('lokacija', ''),
                prihod=prihod,
                odhod=odhod,
                uporabnisko_ime=t['uporabnisko_ime'],
                registrska_stevilka=t['registrska_stevilka']
            )
            rezervacije.append(r)
        return rezervacije



    
    def dodaj_rezervacijo(self, rezervacija: Rezervacija):
        cursor = self.conn.cursor()
        sql = """
        INSERT INTO rezervacija 
        (id_parkirnega_mesta, uporabnisko_ime, registrska_stevilka, prihod, odhod, lokacija)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            rezervacija.id_parkirnega_mesta,
            rezervacija.uporabnisko_ime,
            rezervacija.registrska_stevilka,
            rezervacija.prihod,
            rezervacija.odhod,
            rezervacija.lokacija   
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

  


    def dobi_rezervacije(self) -> List[Rezervacija]:
            self.cur.execute("""
                SELECT r.*, p.lokacija
                FROM rezervacija r
                JOIN parkirisca p ON r.id_parkirnega_mesta = p.id
            """)
            rows = self.cur.fetchall()
            rezervacije = []
            for t in rows:
                prihod = t['prihod']
                odhod = t['odhod']
                if isinstance(prihod, time):
                    prihod = datetime.combine(datetime.today(), prihod)
                if isinstance(odhod, time):
                    odhod = datetime.combine(datetime.today(), odhod)
                
                r = Rezervacija(
                    id_parkirnega_mesta=t['id_parkirnega_mesta'],
                    lokacija=t['lokacija'],
                    prihod=prihod,
                    odhod=odhod,
                    uporabnisko_ime=t['uporabnisko_ime'],
                    registrska_stevilka=t['registrska_stevilka']
                )
                rezervacije.append(r)
            return rezervacije


 
    def dobi_zasedena_mesta(self, lokacija: str) -> List[int]:
        now = datetime.now().time()
        self.cur.execute("""
            SELECT id_parkirnega_mesta
            FROM rezervacija
            WHERE lokacija = %s
            AND prihod::time <= %s::time
            AND odhod::time >= %s::time

        """, (lokacija, now, now))
        rows = self.cur.fetchall()
        return [r['id_parkirnega_mesta'] for r in rows]
    
    def dobi_rezervacije_uporabnika(self, uporabnisko_ime: str) -> List[Rezervacija]:
        self.cur.execute("""
            SELECT * FROM rezervacija WHERE uporabnisko_ime = %s
        """, (uporabnisko_ime,))
        rows = self.cur.fetchall()
        return [Rezervacija.from_dict(row) for row in rows]  # če imaš from_dict, ali ustrezno pretvorbo


    def odstrani_rezervacijo(self, rezervacija_id: int) -> None:
        self.cur.execute("DELETE FROM rezervacija WHERE id = %s", (rezervacija_id,))
        self.conn.commit()

    def dobi_rezervacijo(self, rezervacija_id: int) -> Rezervacija:
        self.cur.execute("SELECT * FROM rezervacija WHERE id = %s", (rezervacija_id,))
        rows = self.cur.fetchone()
        return [Rezervacija.from_row(row) for row in rows]

    def posodobi_rezervacijo(self, rezervacija: Rezervacija) -> None:
        self.cur.execute("""
            UPDATE rezervacija SET odhod = %s WHERE id = %s
        """, (rezervacija.odhod, rezervacija.id))
        self.conn.commit()


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