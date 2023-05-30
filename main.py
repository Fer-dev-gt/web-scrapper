import argparse
import logging
import news_page_object as news                                             # Importamos el archivo "news_page_object" con el alias 'news'
from common import config                                                   # Importamos la funcion "config" del modulo "common.py"

logging.basicConfig(level=logging.INFO)                                     # Configuramos la manera de hacer logging y mostrarlo en pantalla al cambiarle el "level"
logger = logging.getLogger(__name__)                                        # Obtenemos una referencia a nuestro "logger" y le damos el nombre de nuestro archivo


def _news_scraper(news_site_uid):                                           # Ejecuta el "scrapper" recibe como argumento el "news_site_uid"
  host = config()['news_sites'][news_site_uid]['url']                       # Obtenemos el "host", le pasamos el id que el usuario selecciono y solicitamos la llave "url"
  logging.info('Beginning scraper for {}'.format(host))                     # Mostramos la información del "logging" con el nombre del "host"
  homepage = news.HomePage(news_site_uid, host)                             # Hacemos uso de la clase "HomePage" del archivo "news_page_object" le mandamos como parámetros el "news_site_uid" y el "host" todo eso lo guardamos en la variable "homepage"
  for link in homepage.article_links:                                       # por cada link que exista en "homepage.article_link" lo i,primimos
    print(link)
    

if __name__ == '__main__':                                                  # Entry Point
  parser = argparse.ArgumentParser()                                        # Instanciamos un objeto de la clase ArgfParser

  news_site_choices = list(config()['news_sites'].keys())                   # Nos regresa un iterador lo convertimos en una lista con los "keys" de "news_site_choices"
  parser.add_argument('news_site',                                          # Añadimos varias opciones
                      help='The news site that you want to scrape',
                      type=str,
                      choices=news_site_choices)                            # Las opciones que estan en "config.yaml" en el mapa "news_site_choices" que convertimos a lista arriba
  args = parser.parse_args()                                                # Le pedimos al "parser" que los parsee y nos de un objeto con ellos
  _news_scraper(args.news_site)                                             # Comenzamos nuestro "scrapper"