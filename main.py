"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Markéta Boháčková
email: bohackovama@gmail.com
"""
import requests
import bs4 as bs
import csv
import sys

def posli_pozadavek_get(url: str) -> str:
    ''' funkce posle pozadavek na server a vrati odpoved '''
    try:
        response = requests.get(url)
   # Pokud status je 200, ale obsah obsahuje "Page not found"
        if response.status_code == 200:
            if "Page not found" in response.text:
                print(f"Chyba: Stránka nebyla nalezena (obsahuje 'Page not found') na URL: {url}")
                sys.exit()  # Ukončí program
        # Zkontrolujeme další HTTP chyby
        response.raise_for_status()
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP chyba: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Chyba požadavku: {req_err}")
    except Exception as err:
        print(f"Došlo k neočekávané chybě: {err}")  
    else:
        # Pokud žádná chyba nenastala, vrátí obsah odpovědi
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
    return [td_tag.get_text().strip() for td_tag in td_tagy]

def rozsirit_url_kod_obce(url_kod_obce : dict, nazev_obce : list) -> dict:
    ''' funkce rozsiri dict url_kod_obce o nazev obce '''
    return {kod: (url_kod_obce[kod], nazev) for kod, nazev in zip(url_kod_obce.keys(), nazev_obce)}

def ziskej_info_obce(url: str = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103") -> dict:
    ''' funkce ziska info o obcich zadaneho uzemniho celku a vytvori z nich slovnik '''
    odpoved = posli_pozadavek_get(url)
    rozdelene_html = ziskej_parsovanou_odpoved(odpoved)
    td_tagy_odkazy = vyber_vsechny_tagy(rozdelene_html, "td", {"class" :"cislo"})
    td_tagy_nazev = vyber_vsechny_tagy(rozdelene_html, "td", {"class" : "overflow_name"})
    url_kod_obce = ziskej_url_kod_obci(td_tagy_odkazy)
    nazev_obce = ziskej_nazev_obci(td_tagy_nazev)
    return rozsirit_url_kod_obce(url_kod_obce, nazev_obce)

def ziskej_nazvy_atributu(obce_info: dict) -> list:
    ''' funkce vrati nazvy atributu u prvni obce v seznamu'''
    kod_prvni_obce = next(iter(obce_info))
    url = obce_info[kod_prvni_obce][0]
    odpoved_obec = posli_pozadavek_get(url)
    rozdelene_html_obec = ziskej_parsovanou_odpoved(odpoved_obec) 
    atributy_nazvy = [
    ("th", {"id": "sa2"}),
    ("th", {"id": "sa3"}),
    ("th", {"id": "sa6"}),
    ("td", {"headers": "t1sa1 t1sb2"}),
    ("td", {"headers": "t2sa1 t2sb2"})
    ]
    nazvy_atributu = ["Název obce"]
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
        hodnoty  = [nazev]
        odpoved_obec = posli_pozadavek_get(url)
        rozdelene_html_obec = ziskej_parsovanou_odpoved(odpoved_obec)
        for tag, atributy in atributy_hodnoty:
            tagy = vyber_vsechny_tagy(rozdelene_html_obec, tag, atributy)
            for tag in tagy:
                text_content = tag.get_text(separator=" ").strip()
                hodnoty.append(text_content)
        vsechny_obce.append(hodnoty)
    return vsechny_obce

def uloz_data_do_csv(nazev_souboru: str, nazvy_atributu: list, hodnoty_obce: list):
    ''' funkce ulozi data do csv souboru '''
    with open(nazev_souboru, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(nazvy_atributu)
        for hodnoty in hodnoty_obce:
            writer.writerow(hodnoty)
    print(f"Data byla uložena do souboru: {nazev_souboru}")

def nacti_argumenty():
    ''' funkce nacte argumenty z prikazove radky a spusti zpracovani dat '''
    if len(sys.argv) != 3:
        print(
            "Pro spuštění chybí argumenty 'url okresu', 'nazev souboru',",
            "Zapiš: python main.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'Prostejov.csv'", sep="\n"
        )
    elif not sys.argv[1].startswith("https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj="):
        print(
            "Zadali jste špatný formát URL",
            "Zapiš: python main.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'Prostejov.csv'", sep="\n"
            )
    elif not sys.argv[2].endswith(".csv"):
        print("Zadali jste špatný formát souboru")
    else:
        print("Zpracovávám data...")
        obce_info = ziskej_info_obce(sys.argv[1])
        nazvy_atributu = ziskej_nazvy_atributu(obce_info)
        hodnoty_obce = ziskej_hodnoty_obce(obce_info)
        uloz_data_do_csv(sys.argv[2],nazvy_atributu,hodnoty_obce)  
    
if __name__ == "__main__":
    nacti_argumenty()
    
            
