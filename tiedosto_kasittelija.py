import time
from datetime import datetime
import math
import json

PER_SIVU = 10

def tallenna_historia(historia, tiedosto_nimi):
    """
    Tallentaa aikaisemmat pelit tiedostoon
    """
    try:
        with open(tiedosto_nimi, "w") as target:
            json.dump(historia, target)
    except IOError:
        print("Ei voitu avata tiedostoa. Tallennus epaonnistui")


def lataa_historia(tiedosto_nimi):
    """
    Lataa aikaisemmat pelit tiedostosta listaan.
    Jos ei ole pelejä niin palauttaa tyhjän listan
    """
    arr = []
    
    try:
        with open(tiedosto_nimi) as source:
            arr = json.load(source)
    except (IOError, json.JSONDecodeError):
        print("Ei voitu avata tiedostoa. Luodaan tyhja kokoelma")

    return arr


def nayta_historia(historia):
    """
    Nayttaa pelihistorian terminaalissa.
    """
    sivut = math.ceil(len(historia) / PER_SIVU)
    for i in range(sivut):
        alku = i * PER_SIVU
        loppu = (i + 1) * PER_SIVU
        formatoi_sivu(historia[alku:loppu], i)
        if i < sivut - 1:
            input("/paina ENTER jatkaaksesi/")


def formatoi_sivu(rivit, sivu):
    """
    Edelliset pelit formatoidaan per rivi. 1peli=1rivi
    """
    for i, tulos in enumerate(rivit, sivu * PER_SIVU + 1):
        print("{i:2}. Aloitettu: {alku}. Pelin kesto: ({duration}). Pelin tulos: *{peli_tulos}*. Loydetyt miinat: {loydetyt_miinat} ja Miinoja jai: {jaadyt_miinat}. Klikkauksien maara: {painallukset}.".format(
            i=i,
            alku=tulos["aloitus_pvm"],
            duration=time.strftime("%H:%M:%S", time.gmtime(
                tulos["lopetus_aika"]-tulos["aloitus_aika"])),
            peli_tulos=tulos["peli_tulos"],
            loydetyt_miinat=tulos["miinat_loydetty"],
            jaadyt_miinat=tulos["miinat_jaljella"],
            painallukset=tulos["painallukset"]
        ))