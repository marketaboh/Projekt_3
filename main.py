"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Markéta Boháčková
email: bohackovama@gmail.com
"""
import requests
import bs4 as bs

def posli_pozadavek_get(url: str) -> str:
    ''' funkce posle pozadavek na server a vrati odpoved '''
    response = requests.get(url)
    return response.text

def ziskej_parsovanou_odpoved(odpoved_serveru: str) -> bs.BeautifulSoup:
    ''' funkce zpracuje odpoved serveru a vrati ji '''
    return bs.BeautifulSoup(odpoved_serveru, features="html.parser")

def vyber_vsechny_tagy(rozdelene_html, tag: str, attributes: str) -> bs.element.ResultSet:
    ''' funkce vybere vsechny tagy "td" podle zadane tridy '''
    return rozdelene_html.find_all(tag, attributes)

def ziskej_url_kod_obci(td_tagy : bs.element.ResultSet) -> dict:
    ''' funkce vrati url obce z tagu "td" upravi url a vytahne kod obce'''
    url_kod_obce = {}
    for td_tag in td_tagy:
        kod_obce = td_tag.get_text().strip()
        odkaz = f"https://www.volby.cz/pls/ps2017nss/{td_tag.a["href"]}"   # Extract the URL
        url_kod_obce[kod_obce] = odkaz  # ulozeni do slovniku
    return url_kod_obce

def ziskej_nazev_obci(td_tagy : bs.element.ResultSet) -> list:
    ''' funkce vrati nazev obce z tagu "td" '''
    nazev_obce = []
    for td_tag in td_tagy:
        nazev = td_tag.get_text().strip()
        nazev_obce.append(nazev)  # ulozeni nazvu obce do listu
    return nazev_obce

def rozsirit_url_kod_obce(url_kod_obce : dict, nazev_obce : list) -> dict:
    ''' funkce rozsiri dict url_kod_obce o nazev obce '''
    for kod, nazev in zip(url_kod_obce.keys(), nazev_obce):
        url_kod_obce[kod] = (url_kod_obce[kod], nazev)
    return url_kod_obce

def ziskej_info_obce(url: str = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103") -> dict:
    ''' funkce ziska info o obcich zadaneho uzemniho celku a vytvori z nich slovnik '''
    odpoved = posli_pozadavek_get(volby_url)
    rozdelene_html = ziskej_parsovanou_odpoved(odpoved)
    td_tagy_odkazy = vyber_vsechny_tagy(rozdelene_html, "td", {"class" :"cislo"})
    td_tagy_nazev = vyber_vsechny_tagy(rozdelene_html, "td", {"class" : "overflow_name"})
    url_kod_obce = ziskej_url_kod_obci(td_tagy_odkazy)
    nazev_obce = ziskej_nazev_obci(td_tagy_nazev)
    obec_info = rozsirit_url_kod_obce(url_kod_obce, nazev_obce)
    return obec_info

def ziskej_nazvy_atributu(obce_info: dict) -> list:
    ''' funkce vrati nazvy atributu u prvni obce v seznamu'''
    kod_prvni_obce = next(iter(obce_info))
    url, nazev = obce_info[kod_prvni_obce]
    odpoved_obec = posli_pozadavek_get(url)
    rozdelene_html_obec = ziskej_parsovanou_odpoved(odpoved_obec) 
    atributy_nazvy = [
    ("th", {"id": "sa2"}),
    ("th", {"id": "sa3"}),
    ("th", {"id": "sa6"}),
    ("td", {"headers": "t1sa1 t1sb2"}),
    ("td", {"headers": "t2sa1 t2sb2"})
    ]
    nazvy_atributu = []
    for tag, atributy in atributy_nazvy:
        tagy = vyber_vsechny_tagy(rozdelene_html_obec, tag, atributy)
        for tag in tagy:
            text_content = tag.get_text(separator=" ").strip()
            nazvy_atributu.append(text_content)
    return nazvy_atributu

def ziskej_hodnoty_obce(obce_info: dict) -> list:
    ''' funkce vrati hodnoty atributu pro vsechny obce '''
    atributy_hodnoty = [
    ("td", {"headers": "sa2"}),
    ("td", {"headers": "sa3"}),
    ("td", {"headers": "sa6"}),
    ("td", {"headers": "t1sa2 t1sb3"}),
    ("td", {"headers": "t2sa2 t2sb3"})
    ]
    vsechny_obce = []
    for kod_obec, (url, nazev) in obce_info.items():
        hodnoty  = []
        hodnoty.append(nazev)
        odpoved_obec = posli_pozadavek_get(url)
        rozdelene_html_obec = ziskej_parsovanou_odpoved(odpoved_obec)
        for tag, atributy in atributy_hodnoty:
            tagy = vyber_vsechny_tagy(rozdelene_html_obec, tag, atributy)
            for tag in tagy:
                text_content = tag.get_text(separator=" ").strip()
                hodnoty.append(text_content)
        vsechny_obce.append(hodnoty)
    return vsechny_obce

volby_url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"

if __name__ == "__main__":
    
    obce_info = ziskej_info_obce(volby_url)
    nazvy_atributu = ziskej_nazvy_atributu(obce_info)
    #print(nazvy_atributu)
    hodnoty_obce = ziskej_hodnoty_obce(obce_info)
    print(hodnoty_obce[0])
