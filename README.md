# Koe-sovellus

Sovelluksen käyttäjä on joko opettaja tai opiskelija. Sovelluksen avulla opettaja voi luoda eri kouluaineiden kokeita, joissa on automaattisesti tarkastettavia tehtäviä. Opettaja näkee koe- ja käyttäjäkohtaiset tilastot. Opiskelijat voivat suorittaa kokeita sekä nähdä tulokset omista suorituksistaan.

## Sovelluksen ominaisuuksia: 
*    Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
*    Ensimmäinen rekisteröityjä on automaattisesti opettaja. Vain opettaja voi lisätä muita opettajia. Muut itse rekisteröityvät ovat automaattisesti opiskelijoita.
*    Sovelluksen etusivu näyttää kirjautumattomalle henkilölle sovelluksen perusidean ja muuta perustietoa. Opiskelijalle ja opettajalle etusivulla näkyy rooliin sopivat perustoiminnallisuudet.
*    Opiskelija voi poistaa oman tilinsä. Opettaja voi poistaa myös muiden käyttäjien tilejä. Tietokannassa on aina oltava vähintään yksi opettaja, eli viimeistä opettajaa ei pysty poistamaan.
*    Opiskelija näkee listan kokeista ja voi suorittaa kokeen. Jos koe on jo suoritettu, näkee hän saamansa koetuloksen, suoritukseen käyttämäänsä ajan, joka näkyy punaisella, jos aikaraja on ylitetty, ja pystyy tarkastelemaan suorituksiaan. Jos koe on jäänyt kesken, pystyy hän jatkamaan suoritusta.
*    Opettaja pystyy lisäämään, poistamaan ja muokkaamaan kouluaineita, koetehtäviä ja kokeita.
*    Opettaja luo uuden kokeen määrittäämällä kokeelle nimen sekä aikarajan, jonka jälkeen hän pystyy lisäämään kokeelle kysymyksiä.
*    Yksittäinen koetehtävä sisältää kysymyksen, sekä tekstikentän, johon tulee kirjoittaa oikea vastaus. Opettaja määrittää kullekin kysymykselle siitä saatavat pisteet, mikäli vastaus on oikein.
*    Opettaja näkee kokeista tilaston, josta näkee kokeen perustiedot, sekä kuinka moni on suorittanut kokeen, näiden tulosten keskiarvon, sekä kuinka monta suoritusta on kesken.
*    Opettaja näkee käyttäjäkohtaisen tilaston, josta näkee loppuun asti suoritetuista kokeista suoritusajankohdan, saadut pisteet sekä suoritukseen käytetyn ajan, joka näkyy punaisella, jos aikaraja on ylitetty. Tilastosta näkee myös tiedon siitä, jos suoritus on kesken.

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
*   Halutessasi voit lisätä sovellukseen testidataa _(psql < test_data.sql)_, jossa on määritetty kaksi aihealuetta, näille molemmille yhdet kokeet, joissa molemmissa muutamia kysymyksiä. Yhtään käyttäjää ei testidata tietokantaan luo.
*   Käynnistä sovellus Koe-sovellus komennolla: _flask run_
*   Huom, ensimmäisen rekisteröimäsi käyttäjän rooli on automaattisesti 'opettaja'