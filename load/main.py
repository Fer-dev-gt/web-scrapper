# Archivo principal que se encarga de subir nuestros datos a la DB SQL
import argparse                                                                         # Importamos 'argparse' porque queremos convertir nuestro script en un programa ejecutable
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from article import Article                                                             # Nos traemos del archivo 'article.py' la clase Article que extiende de la clase Base              
from base import Base, engine, Session                                                  # Nos traemos las variable que declaramos en el archivo 'base'

def main(filename):                                                                     # La función main recibe el 'filename'
  Base.metadata.create_all(engine)                                                      # Esto nos permite generar nuestra 'squema' en nuestra base de datos
  session = Session()                                                                   # Inicializamos nuestra sesion
  articles = pd.read_csv(filename, on_bad_lines='skip', sep=';')                        # Vamos a leer nuestros articulos (filename) usando Pandas

  for index, row in articles.iterrows():                                                # Usamos el método de Pandas 'iterrows()' que nos permite generar un 'loop' adentro de cada una de nuestras filas de nuestro DataFrame que nos data un "index, row"
    logger.info('Loading article uid {} into DB'.format(row['uid']))
    article = Article(row['uid'],                                                       # Generamos nuestro articulos al pasarle nuestros valores al constructor de la Clase Article, siempre usando la notación 'row['value']'
                      row['body'],
                      row['host'],
                      row['newspaper_uid'],
                      row['n_tokens_body'],
                      row['n_tokens_title'],
                      row['title'],
                      row['url'])
    session.add(article)                                                                # Esta instucción ya nos ingresa nuestros articulos a la base de datos

  session.commit()                                                                      # Le damos un commit a la sesion
  session.close()                                                                       # Cerramos la sesion




if __name__ == '__main__':
  parser = argparse.ArgumentParser()                                                        # Inicializamos nuestro parser usando el método ArgumentParser()
  parser.add_argument('filename', help='The file you want to load into the db', type=str)   # Le añadimos un argumento al que llamaremos 'filename' y le damos un string de 'help=' y le decimos que es de tipo str
  args = parser.parse_args()                                                                # 'Parseamos' nuestro argumentos  
  main(args.filename)                                                                       # Ejecutamos nuestra función main con los argumento parseados con nombre filename