from io import TextIOWrapper
import sys
from requests import get
from bs4 import BeautifulSoup as bs
from pathlib import Path
from os import mkdir
from sys import exit
from traceback import print_exc
from json import load

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
  """
  Recupera il numero totali di pagine

  Parametri:
  ---------
  url: str
    l'url a cui eseguire la richiesta
    

  Returns
  -------
  max_page: int
    Il numero totale di pagine
  """

  try:
    req = get(url, headers=headers)
    soup = bs(req.text, 'html.parser')
  except (ConnectionError, Exception):
    handle_exception()

  max_page = soup.find('div', {'class': 'pagination listing-pager'}).find_all('span')[-1].text[-3:]
  return int(max_page)


def open_resource(config: dict, mode: str) -> TextIOWrapper:

  """
  Apre e ritorna il file di configurazione config.json contenente tutte le impostazioni necessarie
  per il corretto funzionamento del programma

  Parametri:
  ---------
    config: dict
      dizionario json contenente tutte le configurazioni

    mode: str
      modalità in cui aprire il file
  
  Returns:
  --------
  rsc_file: TextIOWrapper
    file contenente tutte le configurazioni necessarie

  """

  file_name = config["code_annunci"]
  rsc_fld = config["resource_folder"]
  if are_we_bundle():
    #root = Path(__file__).parent
    root = Path(sys.executable).parent
  else:
    root = Path(__file__).parent.parent
  file = root.joinpath(rsc_fld, file_name)

  if not root.joinpath(rsc_fld).exists():
    mkdir(path=root.joinpath(rsc_fld))

  rsc_file = open(file, mode=mode, newline="")
  print(type(rsc_file))

  return rsc_file


def create_csv_file(config: dict, mode: str) -> TextIOWrapper:
  """
  Crea e ritorna il file csv in cui scrivere

  Parametri:
  ---------
    config: dict
      dizionario json contenente tutte le configurazioni

    mode: str
      modalità in cui aprire il file
  
  Returns:
  --------
  csv_file: TextIOWrapper
    file csv su cui scrivere

  """

  file_name = config["csv_file"]
  if are_we_bundle():
    #curr = Path(__file__)
    curr = Path(sys.executable)
    while curr.parts[-1] != config["base_folder"]:
      curr = curr.parent
  else:
    curr = Path(__file__).parent.parent
  
  file = curr.joinpath(file_name)
  csv_file = open(file, mode=mode, newline='')
  
  return csv_file


def open_log_file(config: dict) -> TextIOWrapper:
  """
  Crea e ritorna un file con permessi di scrittura in caso di errori
  per scrivere il log error

  Parametri:
  ---------
  config: dict
    dizionario json contenente tutte le configurazioni

  Returns:
  --------
  log_file: textIoWrapper
    file su cui scrivere il log error
  """
  log_name = config["log_file"]
  dwnl = Path(sys.executable).home().joinpath('Downloads')
  log_file_path = dwnl.joinpath(log_name)
  try:
    log_file = open(log_file_path, 'w')
  except Exception:
    handle_exception()

  return log_file


def handle_exception() -> None:
  
  """
  In caso di errori a runtime nel programma scrive il traceback
  su file e lo salva nella cartella Download del computer
  """

  config = read_config()
  log = open_log_file(config)
  print_exc(file=log)
  log.close()
  print('Si è verificato un errore. Ho creato un file chiamato \'log\' nella cartella Download. Inviamelo')
  print('Premi ENTER per terminare...')
  input()
  exit()


def are_we_bundle() -> bool:

  """
  Verifica se il programma è in modalità bundle(eseguibile di PyInstaller)
  o in modalità script

  Returns:
  True: bool
    se il programma è eseguito in modalità bundle
  
  False: bool
    se il porgramma è eseguito in modalità script
  """

  if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    return True
  else:
    return False


def read_config() -> dict:

  """
  Apre il file di configurazione, lo salva in un dizionario e ritorna.

  Returns:
  --------
  config_file_json: dict
    dizionario contente il file di configurazione
  """

  if are_we_bundle():
    #config_file_path = Path(__file__).parent.joinpath("resource", 'config.json')
    config_file_path = Path(sys.executable).parent.joinpath("resource", 'config.json')
  else:
    config_file_path = Path(__file__).parent.parent.joinpath("resource", "config.json")
  
  config_file = open(config_file_path, 'r')
  config_file_json = load(config_file)

  return config_file_json

