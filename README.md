# Projekt: Analýza voleb

Tento projekt slouží k analýze volebních výsledků z roku 2017 v rámci Engeto Online Python Akademie.

Skript, umožní vybrat jakýkoliv územní celek z tohoto odkazu:  [volby.cz](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103). Například "X" u Benešova odkazuje na konkrétní stránku s výsledky voleb. Z této stránky stáhne výsledky hlasování pro všechny obce v daném územním celku.

## Autor
- **Jméno**: Markéta Boháčková  
- **Email**: bohackovama@gmail.com

## Požadavky na prostředí
Projekt vyžaduje Python 3. 

## Instalace

1. Naklonujte si tento repozitář:
   ```sh
   git clone https://github.com/marketaboh/Projekt_3.git
   cd ./Projekt_3
   ```

2. Nainstalujte potřebné knihovny:
   ```sh
   pip install -r requirements.txt
   ```

## Použití

Skript `main.py` se spouští z příkazové řádky s parametry:
```sh
python main.py "<URL okresu>" "<nazev_souboru>.csv"
```

Příklad:
```sh
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "Benesov.csv"
```

### Popis funkcionality
1. Skript odešle požadavek na zadanou URL.
2. Extrahuje data o jednotlivých obcích.
3. Uloží výsledky do souboru `.csv`.

## Ukázka výpisu

Při úspěšném spuštění skript vypíše:
```
Zpracovávám data...
Data byla uložena do souboru: Benesov.csv
```

## Ukázka výstupního CSV souboru

```csv
Název obce,Počet voličů,Vydané obálky,Platné hlasy,Strana A,Strana B
Benešov,15000,14000,13500,7000,6500
Jihlava,18000,17000,16000,8000,8000
``` 
