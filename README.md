# <font size="+2"><b>Luontokamera</b></font>

## <b>Synopsis</b>

Projektina on yleisesti liikkeentunnistuskamera tai riistakameratyylinen etänä toimiva staattinen kamera. Kameran täytyy tunnistaa mielellään pienetkin liikkuvat kohteet ja vähäinenkin liike olematta kuitenkaan liian tarkka, jotta oleelliset asiat erotetaan taustahälystä. Ohjelmaan tulee kuitenkin säädettäviä parametreja, jotta liikkeentunnistus voidaan optimoida kulloisiinkin olosuhteisiin sopivaksi.  	Pääelementteinä käytetään USB-webkameraa, Raspberry Pi tietokonetta ja ohjelmointiin perustuvaa liikkeentunnistusta. Videokuva rakentuu yksittäisistä webkameran ottamista otoksista, joita Raspberry Pi vertaa keskenään ja näin tunnistaa muutoksia kuvattavalla alueella. Nopeat muutokset oletetaan liikkeeksi ja liikettä havaittaessa Raspberry Pi lähettää tilanteesta kuvan pilvipalveluun WLAN-yhteyden avulla tai vaihtoehtoisesti tallentaa kuvan USB-muistitikulle.

Kiinnostus projektiin tuli kasvaneesta kiinnostuksestani konenäköön ja tyhjänpanttina lojuneesta webkamerasta. Lisäksi kesämökilläni liikkuvista eläinten jäljistä tuli idea riistakameramaiseen lähestymistapaan, jossa yhdistyy konenäköohjelmointi ja IoT(Internet of Things)-ratkaisut.

## <b>HW-kuvaus</b>

Tietokoneena toimii Raspberry Pi 3, Model B, sisältäen RAM muistia 1 GB:n. Raspberry Pi:ssä on valmiina asennettuna 802.11.b/g/n Wireless LAN adapter, jota käytetään tässä yhteydessä langattomaan verkkoyhteyteen. Virtaa Raspberry Pi saa Micro USB B, liitännän kautta 2.5A, 5.1V, verkkovirrasta taikka muusta riittävästä virtalähteestä USB-liitännällä. 

USB-webkamerana toimii valmiiksi omistamani Microsoft LifeCam HD-3000. Kamera kykenee 720p HD kuvaan ja käyttää TrueColor-kuvanparannustekniikkaa. Käytännössä Raspberry Pi:llä joudutaan käyttämään matalampaa kuvan laatua tehon, tallennuskapasiteetin ja nettikaistan riittämiseksi. Kamera pystyy ottamaan maksimissaan 30 kuvaa/s ja sen kuvaama sektori on 68,5°. Tarkennus onnistuu vain 1,5 metrin päähän, mutta se ei ole tässä niin oleellinen ominaisuus, kun muut häiriötekijät ovat suurempia. Värisyvyys on 24-bittiä. Kamera liitetään kohdekoneeseen USB 2.0 liitännällä. Vaikka tarkoitus olisi käyttää kameraa luontokamerana, käytännössä tämä onnistuu vain Suomen kesälämpötiloissa, koska kamera on luonnollisesti tarkoitettu sisäkäyttöön.

## <b>SW-kuvaus</b>

Kameraa käytetään Python-ohjelmointikielellä. Tähän tarkoitukseen pythoniin on olemassa OpenCV:n BSD-lisenssin avoimen lähdekoodin kirjastoja. OpenCV on juurikin tarkoitettu reaaliaikaiseen konenäkö-ohjelmointiin ja kirjastot sisältävät paljon erilaisia hyödyllisiä funktioita konenäköön ja kuvankäsittelyyn. Koodi toimii ainakin OpenCV 3.1 versiolla ja ehkä uudemmilla, mutta ei esimerkiksi versiolla 2.4.9. 

Kuvia käsitellään käytännössä RGB-matriiseina. Kuvia siis verrataan toisiinsa yksittäisten pikseleiden väriarvojen perusteella. Kun väriarvot muuttuvat tarpeeksi ja tarpeeksi suurella yhtenäisellä alueella, tulkitaan muutokset liikkeeksi näin yksinkertaistetusti. Kuitenkaan tähän operaatioon ei tarvita absoluuttisia värejä, vaan mustavalkokuva on riittävä ja itse asiassa vaatimus pikseleiden vertailuun ja näistä yhdistettävän hahmon tunnistukseen. Pikseleiden muutokselle annetaan raja-arvo, jonka ylittäessä pikseli tulee valkoiseksi, muutoin kuva on musta. Lisäksi näitä repaleisia yhtenäisiä alueita tasoitetaan ja yhdistellään sopivasti virheiden vähentämiseksi. Liikehahmon ympärille lisätään vihreä suorakulmio alkuperäiseen kuvaan liikkeen ja liikkuvan alueen tunnistamiseksi.

Kun liikettä on havaittu, ohjelma lähettää kuvan WLAN:in välityksellä GoogleDriveen pydrivella(tähän tarkoitukseen käyttäjän on lisättävä ohjelman kansioon oman Drivensä OAuth client_secrets.json tiedosto(ohjeet googlesta)). Jos internet-yhteyttä ei ole, ohjelma tallentaa kuvan automaattisesti tunnistetulle ja mountatulle ulkoiselle USB-muistille tai jos tätäkään ei ole tarjolla, kuva tallentuu käyttäjän kotihakemistoon.
