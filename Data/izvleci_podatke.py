import requests
from bs4 import BeautifulSoup
import csv

# URL strani z informacijami o parkiriščih
url = "https://www.lpt.si/parkirisca/informacije-za-parkiranje/prikaz-zasedenosti-parkirisc"

# Pošljemo zahtevo za pridobivanje vsebine strani
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Poišči vse vrstice v tabeli z zasedenostjo parkirišč
rows = soup.find_all('tr')

# Seznam za shranjevanje podatkov
data = []

# Preberi vrstice tabele
for row in rows:
    cols = row.find_all('td')
    
    # Preverimo, da vrstica vsebuje ustrezno število celic (3 td za parkirišče + 4 za zasedenost)
    if len(cols) == 3:
        parkirisce = cols[0].get_text(strip=True)
        
        # Dnevni podatki o prostih parkirnih mestih
        dnevni_prosta = cols[1].find_all('p')[1].get_text(strip=True)
        dnevni_na_voljo = cols[1].find_all('p')[2].get_text(strip=True)
        
        # Abonentski podatki o prostih parkirnih mestih
        abonenti_na_voljo = cols[2].find_all('p')[0].get_text(strip=True)
        abonenti_oddana = cols[2].find_all('p')[1].get_text(strip=True)
        abonenti_prosta = cols[2].find_all('p')[2].get_text(strip=True)
        
        # Dodaj podatke v seznam
        data.append([parkirisce, dnevni_prosta, dnevni_na_voljo, abonenti_na_voljo,
                     abonenti_oddana, abonenti_prosta])


# Zapiši podatke v CSV datoteko
with open('parkirisca_zasedenost.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Parkirišče", "Dnevni prosta", "Dnevni na voljo", 
                     "Abonenti na voljo", "Abonenti oddana", 
                     "Abonenti prosta"])  # Zapisujemo glavo CSV-ja
    writer.writerows(data)

print("Podatki so bili uspešno shranjeni v 'parkirisca_zasedenost.csv'.")
