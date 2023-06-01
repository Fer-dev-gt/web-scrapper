import argparse
import logging
import re                                                                   # Importarmos "re" (Regular Expressions)
import datetime                                                             # Para trabajar con fechas
import csv                                                                  # Para guardar el archivo como un CSV
import news_page_object as news                                             # Importamos el archivo "news_page_object" con el alias 'news'
from common import config                                                   # Importamos la funcion "config" del modulo "common.py"
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

logging.basicConfig(level=logging.INFO)                                     # Configuramos la manera de hacer logging y mostrarlo en pantalla al cambiarle el "level"
logger = logging.getLogger(__name__)                                        # Obtenemos una referencia a nuestro "logger" y le damos el nombre de nuestro archivo

is_well_formed_link = re.compile(r'^https?://.+/.+$')                       # Definimos el formato que debe tener un link valido. Ejemplo del tipo de patron que acepta la Expresión Regular "https://example.com/hello"
is_root_path = re.compile(r'^/.+$')                                         # Definimos el formato de los links que se basa a la raiz (root). Ejemplo: /some-text
is_other_host = re.compile(r'^https?://.+/$')


def _news_scraper(news_site_uid):                                           # Ejecuta el "scrapper" recibe como argumento el "news_site_uid"
  host = config()['news_sites'][news_site_uid]['url']                       # Obtenemos el "host", le pasamos el id que el usuario selecciono y solicitamos la llave "url"
  logging.info('Beginning scraper for {}'.format(host))                     # Mostramos la información del "logging" con el nombre del "host"
  homepage = news.HomePage(news_site_uid, host)                             # Hacemos uso de la clase "HomePage" del archivo "news_page_object" le mandamos como parámetros el "news_site_uid" y el "host" todo eso lo guardamos en la variable "homepage"

  articles = []                                                             # Voy a guardar la lista de mis articulos encontrados, (lista de objetos)
  for link in homepage.article_links:                                       # por cada link que exista en "homepage.article_link" 
    print(link)
    article = _fetch_article(news_site_uid, host, link)                     # Guardamos el resultado de la función "_fetch_article" que nos permite construir un link al cual podremos acceder y nos ayudara a guardar nuestros datos en un archivo csv

    if article:                                                             # Si exite un articulo, mostramos un mensaje de confirmación
      logger.info('Article fetched!!!')
      articles.append(article)                                              # Agregamos el articulo a mi lista de articulos
      print(article.title)
  print('Número de articulos encontrados: {}'.format(len(articles)))        # Imprimo el número de articulos que logramos obtener

  _save_articles(news_site_uid, articles)                                   # Invocamos la función para guardar los datos, le mandamos como parámetros los "news_site_uid" y "articles" que es la lista de objetos de los articulos validos que encontro


def _save_articles(news_site_uid, articles):                                # Guarda los archivos del Scrapper al crear un archivo CSV, recibe el "News_site_uid" y la lista de objetos de articulos encontrados validos 
  now = datetime.datetime.now().strftime('%Y_%m_%d')                        # Utilizamos la librería "datetime" que nos ayudara a darle el nombre al archivo con la fecha de cuando hicimos el Scrapping, usamos el metodo ".strftime()" para que no nos muestre los segundo, minutos y hora, solo el año, mes y día
  out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(         # Creamos el formato para el nombre de nuestro archivo CSV
    news_site_uid=news_site_uid, datetime=now)
  csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))       # Creamos los Headers para el CSV, usamos "filter()" para tener acceso a @property, usamos una función lambda y vamos a filtrar todas las "propiedades (@property)" que empiecen con "_", y le pasamos cualquier articulo que queramos como "dir(articles[0])" y de ultimo todo ese resultado los pasamos a una lista con "list()"

  with open(out_file_name, mode='w+') as file:                              # Abrimos el archivo "out_file_name" con el modo "w+" que instruye que es para escribir y si no existe el archivo lo tiene que crear y definimos la referencia la archivo como "file"
    writer = csv.writer(file)                                               # Creamos un "writer" de CSV le pasamos el "file" y lo guardamos
    writer.writerow(csv_headers)                                            # Le decimos al "writer" que escriba a la primera columna los Headers

    for article in articles:                                                # Guardamos todos nuestros articulos
      row = [str(getattr(article, property)) for property in csv_headers]   # Nos garantiza que todas las propiedades las vamos a poder guardar (for prop in csv_headers)
      writer.writerow(row)                                                  # Lo escribimos en el row



def _fetch_article(news_site_uid, host, link):                              # Nos retorna un article para luego guardarlo en un csv, recibe 3 parametros
  logger.info('Start fetching article at {}'.format(link))                  
  article = None                                                            # Inicializamos el article como None

  try:                                                                      # Como haremos solicitudes HTTP vamos a manejar ciertos errores con un try/except
    article = news.ArticlePage(news_site_uid, _build_link(host, link))      # Creamos una instancias de "ArticlePage", recibe 2 parámetros el "news_site_uid" y un link que lo obtendremos de la función "_build_link"
  except (HTTPError, MaxRetryError) as error:                               # Manejos 2 errores, si no encuentra el articulo "HTTPError" y "MaxRetryError" cuando intenta ir al infinito cuando intenta acceder a la URL
    logger.warning('Error while fetching the article', exc_info=False)      # Muestro un mensaje personalizado y le digo que la otra info tecnica no la muestre (Para no mostrar mucho texto)
  
  if article and not article.body:                                          # Si encontramos un articulo pero este articulo no tiene un "body" (contenido de la noticia), mostramos un mensaje y no retornamos nada (None)
    logger.warning('Invalid article. There is no body')
    return None
  
  return article                                                            # Si todo sale bien retornamos el articulo que contiene un "body"


def _build_link(host, link):                                                # Verifica que el link tenga buen formato y si no lo tiene le coloca ese formato, recibe como parámetros el "host" y "link"
  if is_well_formed_link.match(link):                                       # Si el link esta buen planteado simplemente lo retornamos
    return link
  elif is_other_host.match(link):                                           # Para que no concatee dos links que empiezan con "https://"
    return link
  elif is_root_path.match(link):                                            # Si el link comienza con diagonal le damos un formato ideal que empieze con el "host" y luego el "link". Ejemplo: https://Hostname/example
    return '{}{}'.format(host, link)
  else:                                                                     # Si no cumple con ningun otro formato lo devolvemos con esta forma
    return '{host}/{uri}'.format(host=host, uri=link)
  


if __name__ == '__main__':                                                  # Entry Point
  parser = argparse.ArgumentParser()                                        # Instanciamos un objeto de la clase ArgfParser

  news_site_choices = list(config()['news_sites'].keys())                   # Nos regresa un iterador lo convertimos en una lista con los "keys" de "news_site_choices"
  parser.add_argument('news_site',                                          # Añadimos varias opciones
                      help='The news site that you want to scrape',
                      type=str,
                      choices=news_site_choices)                            # Las opciones que estan en "config.yaml" en el mapa "news_site_choices" que convertimos a lista arriba
  args = parser.parse_args()                                                # Le pedimos al "parser" que los parsee y nos de un objeto con ellos
  _news_scraper(args.news_site)                                             # Comenzamos nuestro "scrapper" 