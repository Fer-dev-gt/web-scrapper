import bs4
import requests
from common import config                                                           # Importamos del archivo 'common' la función que nos da acceso a nuestra configuración


class HomePage:                                                                     # Esta clase va a representar la página principal de nuestra web

  def __init__(self, news_site_uid, url):                                           # Método para inicializarlo, recibe 3 parámetros, el "self", la "url" y el id del sitio de noticias
    self._config = config()['news_sites'][news_site_uid]                            # Obtenemos una referencia a nuestra configuración llamando a la función "config()" y accedemos a nuestra primera llave del diccionario "[news_sites]" le pasamos el id que estamos usando como parámetro "[news_site_uid]"
    self._queries = self._config['queries']                                         # Vamos a obtener "queries" de la configuración de arriba y le decimos que queremos esas "queries" y la guardamos en la variable 'self._queries'
    self._html = None                                                               # Inicializamos una variable para el html "self._html" y la asignamos como None
    self._visit(url)                                                                # Llamamos a nuestro método "_visit(url)" y le damos la url que usamos al ejecutar el programa

  @property                                                                         # Con esto generamos nuestra primera propiedad
  def article_links(self):                                                          # Función que computa los 'Article Links'
    link_list = []                                                                  # Declaramos una lista vacía
    for link in self._select(self._queries['homepage_article_links']):              # Por cada link en "self._select con parámetro (self._queries)" que contiene los 'homepage_article_links' para obtener los links
      if link and link.has_attr('href'):                                            # Si existe un link dentro de la página y si ese link tiene el atributo "href" (osea si es un link) 
        link_list.append(link)                                                      # Lo añadimos a nuestra lista 'link_list' usando el método "append()"
    return set(link['href'] for link in link_list)                                  # Regresamos nuestro "link_list" pero con una modificación para eliminar cualquier repetido al transformarlo en un 'set' con cada "href" por cada link en nuestra lista de link

  def _select(self, query_string):                                                  # Función auxiliar que nos ayudara a obtener información del objeto que acabamos de "parsear", recibe un 'query_string'
    return self._html.select(query_string)                                          # Retorna la variable 'self._html' con el método ".select()" con el parámeto del "query_string"

  def _visit(self, url):                                                            # Método para visitar la página para hacer "web scrapping", recibe como parámetro la url de la página deseada      
    response = requests.get(url)                                                    # Hacemos la solicitud web con la librería "request" y la guardamos en la variable 'response'
    response.raise_for_status()                                                     # Usamos el método ".raise_for_status()" que muestra un erros si la solicitud no fue concluida correctamente
    self._html = bs4.BeautifulSoup(response.text, 'html.parser')                    # Si todo esta bien con la solicitud, hacemos uso de la librería "Beautiful soup" y le mandamos el texto de la respuesta 'response.text', y el 'html.parser', genera un árbol de html


