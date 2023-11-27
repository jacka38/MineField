import haravasto, tiedosto_kasittelija
import random
import tulvataytto
import os
import platform
import time
from datetime import datetime

#Muuttujat
historia = []
vapaana = []
TULOKSET_TIEDOSTO = "tulokset.json"

#Sanakirja pelin tilastoille
tilastot = {
    "aloitus_aika": 0,
    "lopetus_aika": 0,
    "aloitus_pvm": 0,
    "lopeus_pvm": 0,
    "miinat": 0,
    "miinat_jaljella": 0,
    "miinat_loydetty": 0,
    "peli_tulos": "",
    "painallukset": 0
}

#Miinaharavan sanakirja
tila = {
    "kentta": [],
    "tyhja_kentta": [], 
    "peli": True,
    "painallus_yksi": False,
    "miinat": 0,
    "voitto": 0,
    "peli_voitto": False,
    "kaikki_avattu": 0,
    "leveys": 0,
    "korkeus": 0,
}

def tyhjaa_kentta(tila):
    """
    Resetoi pelikentän, kun aloitetaan peli.
    Varmistaa, että pelin muistiin ei jää edellisiä pelejä.
    """
    tila["kentta"] = []
    tila["tyhja_kentta"] = []
    tila["peli"] = True
    tila["painallus_yksi"] = False
    tila["miinat"] = 0
    tila["voitto"] = 0
    tila["peli_voitto"] = False
    tila["kaikki_avattu"] = 0
    tila["leveys"] = 0
    tila["korkeus"] = 0
    tilastot["painallukset"] = 0
    tilastot["miinat_loydetty"] = 0
    tilastot["miinat_jaljella"] = 0

def laske_miinat(x, y, arr):
    """
    Laskee ruudu lähellä olevat miinat
    """
    luku = 0
    on_miina = arr[y][x] == "x"
    
    if on_miina:
        return None

    vasen = x == 0
    oikea = x == len(arr[0]) - 1
    yla = y == 0
    ala = y == len(arr) - 1

    if vasen and yla and len(arr) > 1:
        for i in arr[:2]:
            for j in i[:2]:
                if j == "x":
                    luku += 1

    elif oikea and yla:
        for i, arr_i in enumerate(arr[:2]):
            for j, arr_j in enumerate(arr_i[x - 1:x + 1]):
                if arr_j == "x":
                    luku += 1

    elif vasen and ala:
        for i in arr[-2:]:
            for j in i[:2]:
                if j == "x":
                    luku += 1

    elif oikea and ala:
        for i, arr_i in enumerate(arr[-2:]):
            for j, arr_j in enumerate(arr_i[-2:]):
                if arr_j == "x":
                    luku += 1

    elif not (vasen or oikea) and yla:
        for i in arr[y:y + 2]:
            for j in i[x - 1:x + 2]:
                if j == "x":
                    luku += 1

    elif not (vasen or oikea) and ala:
        for i in arr[y - 1:y + 1]:
            for j in i[x - 1:x + 2]:
                if j == "x":
                    luku += 1

    elif vasen and not (yla or ala):
        for i in arr[y - 1:y + 2]:
            for j in i[x:x + 2]:
                if j == "x":
                    luku += 1

    elif oikea and not (yla or ala):
        for i in arr[y - 1:y + 2]:
            for j in i[x - 1:x + 1]:
                if j == "x":
                    luku += 1

    else:
        for i in arr[y - 1:y + 2]:
            for j in i[x - 1:x + 2]:
                if j == "x":
                    luku += 1
    return luku

def miinoita(kentta, ruutu, miina_numero):
    """
    Sijoittaa miinat ruutuihin
    """
    for i in range(miina_numero):
        miina = random.choice(ruutu)
        kentta[miina[0]][miina[1]] = "x"
        ruutu.remove(miina)

def piirra_kentta():
    """
    Piirtaa kentan lista muodossa
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.aloita_ruutujen_piirto()

    if tila["peli"] == True:
        for y, sarake in enumerate(tila["kentta"]):
            for x, rivi in enumerate(sarake):
                haravasto.lisaa_piirrettava_ruutu(tila["tyhja_kentta"][y][x], x * 40, y * 40)
        haravasto.piirra_ruudut()

    elif not tila["peli"] and tila["peli_voitto"]:
        for y, sarake in enumerate(tila["kentta"]):
            for x, rivi in enumerate(sarake):
                haravasto.lisaa_piirrettava_ruutu(tila["tyhja_kentta"][y][x], x * 40, y * 40)
        haravasto.piirra_ruudut()
        haravasto.piirra_tekstia("SINÄ VOITIT", 0, 0, (0, 255, 0, 255),)

    else:
        for y, sarake in enumerate(tila["kentta"]):
            for x, rivi in enumerate(sarake):

                haravasto.lisaa_piirrettava_ruutu(tila["tyhja_kentta"][y][x], x * 40, y * 40)
        haravasto.piirra_ruudut()
        haravasto.piirra_tekstia("SINÄ HÄVISIT", 0, 0, (255, 0, 0, 255),)

def luo_kentta():
    """
    Luo pelikentän pelaajan antamilla kokonaisluvuilla.
    """
    print("Anna pelikentan leveys, korkeus ja miinojen maara kokonaislukuna!")
    while True:
        try:
            tila["leveys"] = int(input("Syota kentan LEVEYS:  "))
            tila["korkeus"] = int(input("Syota kentan KORKEUS: "))
            tila["miinat"] = int(input("Syota MIINOJEN lukumaara: "))
            tilastot["miinat"] = tila["miinat"]
        except ValueError:
            print("leveys, korkeus ja miinojen pitaa olla kokonaislukuna")
        else:

            #Pelin alku
            tilastot["aloitus_aika"] = time.time()
            tilastot["aloitus_pvm"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


            #Alustaa muuttuvan kentan
            for rivi in range(tila["korkeus"]):
                tila["tyhja_kentta"].append([])
                for sarake in range(tila["leveys"]):
                    tila["tyhja_kentta"][-1].append(" ")


            #Alustaa kentan miinojen kanssa
            for rivi in range(tila["korkeus"]):
                tila["kentta"].append([])
                for sarake in range(tila["leveys"]):
                    tila["kentta"][-1].append(" ")

            #Alusta mahdolliset ruudut
            for x in range(tila["korkeus"]):
                for y in range(tila["leveys"]):
                    vapaana.append((x, y))
            break


def ruutu_numero(kentta):
    """
    Laskee montako miinaa ruudun lahella on
    jos ei ollenkaan niin tyhja ruutu
    """
    for i, rivi in enumerate(tila["kentta"]):
        for j, sarake in enumerate(rivi):
            miinat = laske_miinat(j, i, tila["kentta"])
            if miinat != None:
                if miinat == 0:
                    tila["kentta"][i][j] = " "
                else:
                    tila["kentta"][i][j] = miinat

def peli_lopetus(tila, tilastot):
    """
    Tallentaa pelin tulokset pelin päättyessä
    """
    if not tila["peli"]:
        historia = tiedosto_kasittelija.lataa_historia(TULOKSET_TIEDOSTO)
        historia.append(tilastot)
        tiedosto_kasittelija.tallenna_historia(historia, TULOKSET_TIEDOSTO)

        haravasto.lopeta()

def tarkista_voitto(tila, tilastot):
    """
    Tarkistaa voittiko pelaaja pelin.
    """
    voitto_lkm = 0
    avoinna_lkm = 0

    for i, val in enumerate(tila["tyhja_kentta"]):
        for j, val_2 in enumerate(val):
            if (tila["tyhja_kentta"][i][j] == " " and tila["kentta"][i][j] == "x") or (tila["tyhja_kentta"][i][j] == "f" and tila["kentta"][i][j] == "x"):
                voitto_lkm += 1
            elif tila["tyhja_kentta"][i][j] != " " and tila["tyhja_kentta"][i][j] != "f":
                avoinna_lkm += 1

    if voitto_lkm == tila["miinat"] and avoinna_lkm == (tila["korkeus"] * tila["leveys"] - tila["miinat"]):
        for i, val in enumerate(tila["tyhja_kentta"]):
            for j, val_2 in enumerate(val):
                if tila["tyhja_kentta"][i][j] == " " and tila["kentta"][i][j] == "x":
                    tila["tyhja_kentta"][i][j] = "f"
        tila["peli"] = False
        tila["peli_voitto"] = True
        tilastot["lopetus_aika"] = time.time()
        tilastot["lopeus_pvm"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tilastot["peli_tulos"] = "VOITTO"
        tilastot["miinat_loydetty"] = tila["miinat"]
        tilastot["miinat_jaljella"] = 0

        historia = tiedosto_kasittelija.lataa_historia(TULOKSET_TIEDOSTO)
        historia.append(tilastot)
        tiedosto_kasittelija.tallenna_historia(historia, TULOKSET_TIEDOSTO)

    tila["voitto"] = 0
    tila["kaikki_avattu"] = 0

def ensimmainen_painallus_kasittelija(x, y, tila, vapaana):
    """
    Käsittelee pelaajan 1. klikkauksen, joka ei voi ikinä olla miina.
    """
    if not tila["painallus_yksi"]:
        vapaana.remove((int(y/40), int(x/40)))
        miinoita(tila["kentta"], vapaana, tila["miinat"])
        ruutu_numero(tila["kentta"])
        tila["painallus_yksi"] = True

def miina_painallus_kasittelija(x, y, tila, tilastot):
    """
    Käsittelee pelaajan miinaan klikkaamisen.
    """
    if tila["kentta"][int(y/40)][int(x/40)] == "x":
        tila["peli"] = False
        tilastot["lopetus_aika"] = time.time()
        tilastot["lopeus_pvm"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tilastot["peli_tulos"] = "HAVIO"

        for i, val in enumerate(tila["kentta"]):
            for j, val_2 in enumerate(val):
                if val_2 == "x" and tila["tyhja_kentta"][i][j] != "f":
                    tila["tyhja_kentta"][i][j] = "x"
                    tilastot["miinat_jaljella"] += 1
                if val_2 == "x" and tila["tyhja_kentta"][i][j] == "f":
                    tilastot["miinat_loydetty"] += 1

        historia = tiedosto_kasittelija.lataa_historia(TULOKSET_TIEDOSTO)
        historia.append(tilastot)
        tiedosto_kasittelija.tallenna_historia(historia, TULOKSET_TIEDOSTO)


def hiiri_kasittelija(x, y, nappi, muuttujat):
    """
    Käsittelee pelaajan klikkaukset, olkoon vasen tai oikea hiiri. 
    Pelin logiikkaa käytetään tässä tulvatäyttö, voitto ja häviö.
    """
    # Pelin lopetus
    if not tila["peli"]:
        peli_lopetus(tila, tilastot)

    else:
        if nappi == haravasto.HIIRI_VASEN and tila["tyhja_kentta"][int(y/40)][int(x/40)] != "f":
            
            tilastot["painallukset"] += 1

            #Ensimmaisessa ruudussa ei voi olla miinaa
            ensimmainen_painallus_kasittelija(x, y, tila, vapaana)

            #Miina painallus niin pelin haviaa
            miina_painallus_kasittelija(x, y, tila, tilastot)

            #Tulvataytto, kun tyhja ruutu
            if tila["kentta"][int(y/40)][int(x/40)] == " ":
                tulvataytto.tulvataytto(tila["kentta"], tila["tyhja_kentta"], int(x/40), int(y/40))
            else:
                tila["tyhja_kentta"][int(y/40)][int(x/40)] = tila["kentta"][int(y/40)][int(x/40)]

            #Voitto
            tarkista_voitto(tila, tilastot)

        #Lippu tai lipun poisto
        elif nappi == haravasto.HIIRI_OIKEA:
            if tila["tyhja_kentta"][int(y/40)][int(x/40)] == " ":
                tila["tyhja_kentta"][int(y/40)][int(x/40)] = "f"
            elif tila["tyhja_kentta"][int(y/40)][int(x/40)] == "f":
                tila["tyhja_kentta"][int(y/40)][int(x/40)] = " "

        piirra_kentta()
        haravasto.lataa_kuvat("spritet")

def clear():
    """
    Tyhjentää terminaalin
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def miinaharava():
    """
    Ohjelman käynnistäjä.
    """
    #Uusi tyhja kentta pelille
    tyhjaa_kentta(tila)

    luo_kentta()
    haravasto.luo_ikkuna(len(tila["kentta"][0]) * 40, len(tila["kentta"]) * 40)
    haravasto.lataa_kuvat("spritet")
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
    haravasto.aloita()

def menu(tiedosto):
    """
    Pelin valikko.
    """
    if not os.path.exists(TULOKSET_TIEDOSTO):
        with open(TULOKSET_TIEDOSTO, "w") as uusi_tiedosto:
            pass

    clear()
    print("***Tervetuloa MIINAHARAVA peliin***")

    while True:
        print("\n")
        print("--valitse toiminto--")
        print("1. ALOITA Uusi peli")
        print("2. Tilastot")
        print("3. LOPETA")
        valinta = input("Valitse vaihtoehto (1, 2, 3): ").strip().lower()

        if valinta == "1":
            miinaharava()
        elif valinta == "2":
            historia = tiedosto_kasittelija.lataa_historia(tiedosto)
            tiedosto_kasittelija.nayta_historia(historia)
        elif valinta == "3":
            break
        else:
            print("!!Valittua vaihtoehtoa ei ole!!")

if __name__ == "__main__":
    menu(TULOKSET_TIEDOSTO)