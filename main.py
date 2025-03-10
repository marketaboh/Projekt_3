"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Markéta Boháčková
email: bohackovama@gmail.com
"""
import requests
import bs4 as bs

def posli_pozadavek_get(url):
    ''' funkce posle pozadavek na server a vrati odpoved '''
    response = requests.get(url)
    return response.text

def ziskej_parsovanou_odpoved(odpoved_serveru):
    ''' funkce zpracuje odpoved serveru a vrati ji '''
    return bs.BeautifulSoup(odpoved_serveru, features="html.parser")

def vyber_vsechny_td_tagy(rozdelene_html):
    ''' funkce vybere vsechny tagy "td" s class "cislo" '''
    return rozdelene_html.find_all("td", {"class": "cislo"})

def ziskej_url_obci(td_tagy):
    ''' funkce vrati url obce z tagu "td" '''
    odkazy = []
    for td_tag in td_tagy:
        odkazy.append(td_tag.a["href"])
    return odkazy

def uprav_url(url):
    ''' funkce upravi url obce '''
    obce  = []
    for odkaz in url:
       obce.append(f"https://www.volby.cz/pls/ps2017nss/{odkaz}") 
    return obce   

volby_url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"

if __name__ == "__main__":
    odpoved = posli_pozadavek_get(volby_url)
    rozdelene_html = ziskej_parsovanou_odpoved(odpoved)
    td_tagy = vyber_vsechny_td_tagy(rozdelene_html)
    ref = ziskej_url_obci(td_tagy)
    url_obce = uprav_url(ref)
    #print(url_obce[0])
    for obec in url_obce:
        print(obec)
        odpoved_obec = posli_pozadavek_get(obec)
        rozdelene_html_obec = ziskej_parsovanou_odpoved(odpoved_obec)
       
