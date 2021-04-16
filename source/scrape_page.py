from bs4 import BeautifulSoup as Bs
from requests import get
from utility import headers
from time import sleep
from random import randint


def get_list_annunci(soup: Bs, old_annunci: dict, new_annunci: dict) -> None:

    main_content = soup.find('div', {'id': 'maincontent'})

    for annuncio in main_content.find_all('li'):
        code, link = get_first_detail_annuncio(annuncio)
        if code not in old_annunci.keys():
            new_annunci[code] = {"link": link}


def get_first_detail_annuncio(annuncio) -> tuple:

    code_annuncio = annuncio.find('dd').text
    link_annuncio = annuncio.find_all('a')[-1]['href']

    return code_annuncio, link_annuncio


def get_detailed_annuncio(annunci: dict) -> None:
    index = 1
    for code in annunci.keys():
        print(f'{index} of {len(annunci)}')
        link = annunci[code]['link']
        req = get(link, headers=headers)
        soup = Bs(req.text, 'html.parser')

        get_address(soup, annunci, code)
        get_detail_procedure(soup, annunci, code)
        get_detail_immobile(soup, annunci, code)
        get_detail_vendita(soup, annunci, code)
        get_detail_asta(soup, code, annunci)
        index += 1
        sleep(randint(1, 3))


def get_address(soup, annunci, code):

    indirizzo = str(soup.find('div', {'class': 'detail-top-info'}).h1.text)
    indirizzo_def = indirizzo[indirizzo.find('in')+3:].strip()
    annunci[code]["indirizzo"] = indirizzo_def


def get_detail_procedure(soup, annunci, code):

    section = soup.find_all('section', {'class':'section-detail'})[0]

    descriptions = section.find_all('dt')
    values = section.find_all('dd')

    for pair in zip(descriptions, values):
        description = pair[0].text
        value = pair[1].text
        if description != '':
            annunci[code][description] = str(value).strip()


def get_detail_immobile(soup, annunci, code):

    section = soup.find_all('section', {'class':'section-detail'})[2].find('dl', {'class':'dl-table clearfix'})
    
    descriptions = section.find_all('dt')
    values = section.find_all('dd')

    for pair in zip(descriptions, values):
        description = pair[0].text.strip()
        value = pair[1].text.strip()
        if description != '':
            annunci[code][description] = value
    
    descrizione_imm = soup.find_all('section', {'class':'section-detail'})[2].find('p').text.replace("\n", "").strip()
    
    annunci[code]['descrizione'] = descrizione_imm


def get_detail_vendita(soup, annunci, code):

    section = soup.find_all('section', {'class':'section-detail'})[3]

    descriptions = section.find_all('dt')
    values = section.find_all('dd')

    for pair in zip(descriptions, values):
        description = pair[0].text.strip()
        value = pair[1].text.strip()
        if description != '':
            annunci[code][description] = value


def get_detail_asta(soup, code, annunci):
    
    section = soup.find_all('section', {'class':'section-detail'})[4]

    descriptions = section.find_all('dt')
    values = section.find_all('dd')

    for pair in zip(descriptions, values):
        description = pair[0].text.strip()
        value = pair[1].text.replace("€", "").replace(".", "").strip()
        if description != '':
            annunci[code][description] = value
