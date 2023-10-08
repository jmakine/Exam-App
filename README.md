# Koe-sovellus

Sovelluksen käyttäjä on joko opettaja tai opiskelija. Sovelluksen avulla opettaja voi luoda eri kouluaineiden kokeita, joissa on automaattisesti tarkastettavia tehtäviä. Opettaja näkee koe- ja käyttäjäkohtaiset tilastot. Opiskelijat voivat suorittaa kokeita sekä nähdä tulokset omista suorituksistaan.

## Sovelluksen ominaisuuksia: 
*    Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
*    Ensimmäinen rekisteröityjä on automaattisesti opettaja. Vain opettaja voi lisätä muita opettajia. Muut itse rekisteröityvät ovat automaattisesti opiskelijoita.
*    Käyttäjä voi poistaa oman tilinsä. Opettaja voi poistaa myös muiden käyttäjien tilejä. Tietokannassa on aina oltava vähintään yksi opettaja, eli viimeistä opettajaa ei pysty poistamaan.
*    Opiskelija näkee listan kokeista ja voi suorittaa kokeen. Jos koe on jo suoritettu, näkee hän saamansa koetuloksen, suoritukseen käyttämäänsä ajan, ja pystyy tarkastelemaan suorituksiaan.
*    Opettaja pystyy lisäämään, poistamaan ja muokkaamaan kouluaineita, koetehtäviä ja kokeita.
*    Yksittäinen koetehtävä sisältää kysymyksen, sekä tekstikentän, johon tulee kirjoittaa oikea vastaus. Opettaja määrittää kullekin kysymykselle siitä saatavat pisteet, mikäli vastaus on oikein.
*    Opettaja näkee kokeista tilaston, kuinka moni on suorittanut kokeen sekä tulosten keskiarvon.

### Lisäksi tehtävä vielä:
*   Opettajan 'Käyttäjätilastot' -näkymään suoritukseen käytetty aika näkyviin. Nyt on vasta opiskelijalle näkyvässä suoritustilastossa.
*   Ilmoitukset onnistuneista lisäyksistä ja poistoista puuttuu vielä kokonaan. Opettajalla tämä tarkoittaa uuden kokeen, käyttäjän, aihealueen tai kysymyksen poistamista tai lisäämistä. Opiskelijalla valmiin kokeen lähetystä.
*   Sovelluksen ulkonäkö on yhä melko persoonaton, mutta parempaan päin. Otetaan bootstrapin alerts käyttöön ja korvataan sillä nykyiset virheilmoitukset.
*   Koodin refaktorointia.

## Sovelluksen käyttäminen:
*   Kloonaa repositorio ja navigoi kloonattuun kansioon
*   Luo Pythonin virtuaaliympäristö kansion sisään komennolla: _python -m venv venv_ tai _python3 -m venv venv_
*   Aktivoi virtuaaliympäristö: _source venv/bin/activate_
*   Asenna flask: _pip install flask_
*   Asenna riippuvuudet: _pip install -r requirements.txt_
*   Määritä .env -tiedoston sisältö:
    1.  Aseta PostgreSQL-osoite: 
        DATABASE_URL=postgresql+psycopg2://**ip_address/db**?user=**username**&password=**password**
        (Esim. postgresql+psycopg2://**127.0.0.1/exam_app**?user=**jenni_penni**&password=**123abc**). 
    1.  Aseta salainen avain (jotain satunnaisia merkkejä): 
        SECRET_KEY=abcdefghijklmnop (esimerkkinä, mutta älä käytä tätä)
*   Luo schema.sql -tiedoston mukaiset tietokantataulut PostgreSQL -komentoikkunassa _(psql < schema.sql)_
*   Käynnistä sovellus Koe-sovellus komennolla: _flask run_
*   Huom, ensimmäisen rekisteröimäsi käyttäjän rooli on automaattisesti 'opettaja'