from bs4 import BeautifulSoup as Bs
from utility import get_max_page, open_resource, create_csv_file, are_we_bundle, headers
from scrape_page import get_detailed_annuncio, get_list_annunci
from random import randint
from requests import get
from time import sleep
from csv import DictWriter, QUOTE_ALL
import json


base_url = 'https://aste.immobiliare.it/ricerca-generale/provincia-MI/comune-8042/categoria-1/tipologia-4?pag='
CODE_ANNUNCI_JSON = 'code_annunci.json'
CSV_FILE = 'nuovi annunci.csv'
FIELDNAMES = [
    'Scaricato il', 'Data e ora asta', 'indirizzo', 'Base', 'descrizione', 'link', 'Riferimento Immobile',
    'Tipologia', 'Categoria', 'Procedura', 'Numero Procedura', 'Tribunale', 'Data annuncio', 'Aggiornato il',
    'Tipo vendita', 'Rialzo minimo', 'Stato', 'Deposito cauzionale', 'Giudice', 'Delegato', 'Custode',
    'Telefono custode', 'Luogo vendita', 'Note', 'Esito', 'Curatore', 'Superficie', 'Locali', 'Offerta minima'
    ]


if __name__ == '__main__':
    try:
        old_annunci_file = open_resource(CODE_ANNUNCI_JSON, 'r')
        old_annunci_dict = json.load(old_annunci_file)
    except (json.JSONDecodeError, FileNotFoundError):
        old_annunci_dict = {}
    new_annunci_dict = dict()

    max_page = get_max_page(f'{base_url}{1}')
    OSError
    print(f'Max page: {max_page}')

    for page in range(1, max_page+1):
        print(f'Page: {page}')
        sleep(randint(2, 6))
        req = get(f'{base_url}{page}', headers=headers)
        soup = Bs(req.text, 'html.parser')
        get_list_annunci(soup=soup, old_annunci=old_annunci_dict, new_annunci=new_annunci_dict)

    with open_resource(CODE_ANNUNCI_JSON, 'w') as code_file:
        for new_annuncio in new_annunci_dict.items():
            old_annunci_dict[new_annuncio[0]] = new_annuncio[1]
        json.dump(old_annunci_dict, code_file, indent=4)

    print(f'Nuovi annunci: {len(new_annunci_dict)}')
    get_detailed_annuncio(new_annunci_dict)

    with create_csv_file(CSV_FILE, 'w') as csv_file:
        writer = DictWriter(csv_file, fieldnames=FIELDNAMES, extrasaction="ignore", quoting=QUOTE_ALL, delimiter=";")
        writer.writeheader()
        for code_imm in new_annunci_dict.keys():
            writer.writerow(new_annunci_dict[code_imm])
