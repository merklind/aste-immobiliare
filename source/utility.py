from requests import get
from bs4 import BeautifulSoup as bs
from pathlib import Path

RSC_FOLDER = 'resource'

headers = {
    'authority': 'aste.immobiliare.it',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://aste.immobiliare.it/ricerca-generale/provincia-MI/comune-8042/categoria-1/tipologia-4?pag=8',
    'accept-language': 'it',
    'cookie': 'ASTENSID=8a8b77f28a9cb55f200175d77aa3fd6e; _ga=GA1.3.2134479940.1618392630; _gid=GA1.3.1930963065.1618392630; __utma=221933576.2134479940.1618392630.1618392630.1618392630.1; __utmc=221933576; __utmz=221933576.1618392630.1.1.utmcsr=(direct)^|utmccn=(direct)^|utmcmd=(none); __utmv=221933576.^|5=sitVer=6.2=1; cookieBanner=1; __utmb=221933576.0.10.1618392670516',
}


def get_max_page(url: str) -> int:
  '''
  Ottiene e ritorna il massimo numero di pagine totali degli annunci
  @param url: l'url a cui eseguire la richiesta
  '''

  req = get(url, headers=headers)
  soup = bs(req.text, 'html.parser')

  max_page = soup.find('div', {'class': 'pagination listing-pager'}).find_all('span')[-1].text[-3:]
  return int(max_page)


def open_resource(file_name:str, mode: str):

  rsc_fld = RSC_FOLDER
  root = Path(__file__).parent
  file = root.joinpath(rsc_fld, file_name)

  return open(file, mode=mode, newline="")