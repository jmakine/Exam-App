# Koe-sovellus

Sovelluksen käyttäjä on joko opettaja tai opiskelija. Sovelluksen avulla opettaja voi luoda eri kouluaineiden kokeita, joissa on automaattisesti tarkastettavia tehtäviä. _Opiskelijat voivat suorittaa kokeita. Kesken..._

## Sovelluksen ominaisuuksia: 
*    Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
*    Ensimmäinen rekisteröityjä on automaattisesti opettaja. Vain opettaja voi lisätä muita opettajia. Muut itse rekisteröityvät ovat automaattisesti opiskelijoita.
*    Käyttäjä voi poistaa oman tilinsä. Opettaja voi poistaa myös muiden käyttäjien tilejä. Tietokannassa on aina oltava vähintään yksi opettaja, eli viimeistä ei pysty poistamaan.
*    Opiskelija näkee listan kokeista kouluaineittain _ja voi suorittaa kokeen. Jos koe on jo suoritettu, näkee hän saamansa koetuloksen. Vielä toteuttamatta!_
*    Opettaja pystyy lisäämään, poistamaan ja muokkaamaan kouluaineita, koetehtäviä ja kokeita.
*    Yksittäinen koetehtävä sisältää kysymyksen, sekä tekstikentän, johon tulee kirjoittaa oikea vastaus.
*    _Opettaja näkee kokeista tilaston, kuinka moni on suorittanut kokeen sekä tulosten keskiarvon. Vielä toteuttamatta!_

### Lisäksi tehtävä vielä:
*   Header, jossa kirjautuneen käyttäjän nimi, logout-nappula ja navbar käyttäjäystävällisempää navigointia varten.
*   Validointeja tietokantaan _(ainakin tekstikenttien pituusrajoitukset)_
*   Opiskelijan vastausten tarkistaminen ja koetulosten lisääminen tietokantaan. Vaatii varmaankin vielä yhden taulun.
*   Kokeen aikaraja-toiminnallisuuden toteutus, jos ehtii.

## Sovelluksen käyttäminen:
*   Kloonaa repositorio ja navigoi kloonattuun kansioon
*   Luo Pythonin virtuaaliympäristö kansion sisään komennolla: _python -m venv venv_ tai _python3 -m venv venv_
*   Aktivoi virtuaaliympäristö: _source venv/bin/activate_
*   Asenna flask: _pip install flask_
*   Asenna riippuvuudet: _pip install -r requirements.txt_
*   Määritä .env -tiedoston sisältö:
    1.   Aseta PostgreSQL-osoite: 
        DATABASE_URL=postgresql+psycopg2://**ip_address/db**?user=**username**&password=**password**
        (Esim. postgresql+psycopg2://**127.0.0.1/exam_app**?user=**jenni_penni**&password=**123abc**). 
    1.  Aseta salainen avain (jotain satunnaisia merkkejä): 
        SECRET_KEY=abcdefghijklmnop (esimerkkinä, mutta älä käytä tätä)
*   Luo schema.sql -tiedoston mukaiset tietokantataulut PostgreSQL -komentoikkunassa _(psql < schema.sql)_
*   Käynnistä sovellus Koe-sovellus komennolla: _flask run_
*   Huom, ensimmäisen rekisteröimäsi käyttäjän rooli on automaattisesti 'opettaja'