from bs4 import BeautifulSoup as Bs
from scrape_page import get_detailed_annuncio, get_list_annunci
from utility import get_max_page, open_resource, create_csv_file, headers, read_config
from random import randint
from requests import get
from time import sleep
from csv import DictWriter, QUOTE_ALL
import json


if __name__ == '__main__':
    #carica il file di configurazione, per cambiare impostazioni modificare questo file
    config = read_config()
    try:
        # apre il vecchio file con i codici degli annunci
        old_annunci_file = open_resource(config, 'r')
        # converte il file degli annunci in un dizionario
        old_annunci_dict = json.load(old_annunci_file)
    except (json.JSONDecodeError, FileNotFoundError):
        # se il file non esiste crea un dizionario vuoto
        old_annunci_dict = {}
    # crea dizionario per i nuovi annunci
    new_annunci_dict = dict()

    # ottiene il numero massimo di pagine da cui fare scrape
    max_page = get_max_page(f'{config["base_url"]}{1}')
    print(f'Max page: {max_page}')

    #per ogni pagina ottiene i codici degli annunci
    for page in range(1, max_page+1):
        print(f'Page: {page}')
        sleep(randint(2, 6))
        req = get(f'{config["base_url"]}{page}', headers=headers)
        soup = Bs(req.text, 'html.parser')
        get_list_annunci(soup=soup, old_annunci=old_annunci_dict, new_annunci=new_annunci_dict)

    with open_resource(config, 'w') as code_file:
        for new_annuncio in new_annunci_dict.items():
            old_annunci_dict[new_annuncio[0]] = new_annuncio[1]
        json.dump(old_annunci_dict, code_file, indent=4)

    print(f'Nuovi annunci: {len(new_annunci_dict)}')
    get_detailed_annuncio(new_annunci_dict)

    with create_csv_file(config, 'w') as csv_file:
        writer = DictWriter(csv_file, fieldnames=config["field_names"], extrasaction="ignore", quoting=QUOTE_ALL, delimiter=";")
        writer.writeheader()
        for code_imm in new_annunci_dict.keys():
            writer.writerow(new_annunci_dict[code_imm])
