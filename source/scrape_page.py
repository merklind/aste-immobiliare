from bs4 import BeautifulSoup as Bs
import bs4
from requests import get
from utility import headers
from time import sleep
from random import randint
from datetime import date


def get_list_annunci(soup: Bs, old_annunci: dict, new_annunci: dict) -> None:

	"""
		Esegue lo scrape di 'soup' e aggiunge nel dizionario new_annunci
		tutti gli annunci che non sono presenti nel dizionario old_annunci

		Parametri:
		---------
		soup: Bs
			Pagina su cui fare lo scrape
		
		old_annunci: dict
			dizionario contenente tutte i codici degli annunci già visitati precedentemente

		new_annunci: dict
			dizionario in cui inserire i codici dei nuovi annunci
	"""

	main_content = soup.find('div', {'id': 'maincontent'})

	for annuncio in main_content.find_all('li'):
		code, link = get_first_detail_annuncio(annuncio)
		if code not in old_annunci.keys():
				new_annunci[code] = {"link": link}


def get_first_detail_annuncio(annuncio: bs4.element.Tag) -> tuple:

	"""
		Ottiene il codice dell'annuncio e il link 
		della pagina di dettaglio dell'annuncio

		Returns:
		--------
		code_annuncio: str
			stringa che rappresenta il codice dell'annuncio
		link_annuncio: str
			link alla pagina di dettaglio dell'annuncio
	"""

	code_annuncio = annuncio.find('dd').text
	link_annuncio = annuncio.find_all('a')[-1]['href']

	return code_annuncio, link_annuncio


def get_detailed_annuncio(annunci: dict) -> None:
    index = 1
    today = date.today()
    for code in annunci.keys():
        link = annunci[code]['link']
        print(f'{index} of {len(annunci)}: {link}')
        annunci[code]['Scaricato il'] = today.strftime('%d/%m/%Y')
        req = get(link, headers=headers)
        soup = Bs(req.text, 'html.parser')

        try:
            get_address(soup, annunci, code)
            get_detail_procedure(soup, annunci, code)
            get_detail_immobile(soup, annunci, code)
            get_detail_vendita(soup, annunci, code)
            get_detail_asta(soup, code, annunci)
            index += 1
            sleep(randint(1, 3))
        except:
            print("Errore")


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
        value = str(pair[1].text.strip())
        if description != '':
            if description == 'Data e Ora':
                index_ore = value.find('ore')
                annunci[code]['Data e ora asta'] = f'{value[:index_ore-1]} {value[index_ore+3:]}'
            else:
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
