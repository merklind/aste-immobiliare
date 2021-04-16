from source import CODE_ANNUNCI_JSON, CSV_FILE
from bs4 import BeautifulSoup as Bs
from utils import get_max_page, open_resource, headers
from scrape_page import get_detailed_annuncio, get_list_annunci
from random import randint
from requests import get
from time import sleep
from csv import DictWriter, QUOTE_ALL
import json


base_url = 'https://aste.immobiliare.it/ricerca-generale/provincia-MI/comune-8042/categoria-1/tipologia-4?pag='


if __name__ == '__main__':
    old_annunci_file = open_resource(CODE_ANNUNCI_JSON, 'r')
    try:
        old_annunci_dict = json.load(old_annunci_file)
    except json.JSONDecodeError:
        old_annunci_dict = {}
    new_annunci_dict = dict()

    max_page = get_max_page(f'{base_url}{1}')
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

    fieldnames = []
    for code_imm in new_annunci_dict.keys():
        for key in new_annunci_dict[code_imm].keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with open_resource(CSV_FILE, 'w') as csv_file:
        writer = DictWriter(csv_file, fieldnames=fieldnames, extrasaction="ignore", quoting=QUOTE_ALL, delimiter=";")
        writer.writeheader()
        for code_imm in new_annunci_dict.keys():
            writer.writerow(new_annunci_dict[code_imm])
