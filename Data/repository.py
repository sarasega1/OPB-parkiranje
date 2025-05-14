import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import datetime
import os

from Data.models import Parkirisce
from typing import List

# Preberemo port za bazo iz okoljskih spremenljivk
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

## V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.

class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


        

    def dobi_parkirisca(self) -> List[Parkirisce]:               
        self.cur.execute("""
            SELECT id_parkirisca, st_prostih_mest, lokacija
            FROM Parkirisce
            Order by id_parkirisca desc
        """)
        
        # rezultate querya pretovrimo v python seznam objektov (transkacij)
        parkirisca = [Parkirisce.from_dict(t) for t in self.cur.fetchall()]
        return parkirisca

