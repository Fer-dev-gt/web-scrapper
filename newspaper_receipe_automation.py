import pandas as pd
import argparse                                                                       # Librería para convertir esto en un Script
import logging
from urllib.parse import urlparse
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)                                                  # Obtenemos una refencia de nuestro Logger con ".getLogger(__name__)" con el nombre interno que tiene nuestro archivo


def main(filename):                                                                   # Ejecuta las funciones que limpian y transforman a nuestro DataFrame el cual retornamos, Recibe como argumento al "filename" que habiemos creado como argumento en el Entry Point
  logger.info('Starting cleaning process')
  df = _read_data(filename)                                                           # Leemos los datos y creamos un DataFrame con este función, 'df' significa DataFrame
  newspaper_uid = _extract_newspaper_uid(filename)                                    # Guardamos y extraemos el UID (nombre del periodico) de los articulos de noticias, pasamos el archivo CSV
  df = _add_newspaper_uid_column(df, newspaper_uid)                                   # Modificamos el DataFrame en las columnas le añadimos el UID, recibe 2 parámetros, el DataFrama "df" como lo llevamos trabajando y el valor del UID al cual lo meteremos en el DataFrame
  df = _extract_host(df)                                                              # Extraemos el 'host' del DataFrame (Ej: elpais.com) y lo agregamos como nueva columnas, enviamos el DataFrame
  return df                                                                           # Regresamos el DataFrame "Transformado" al Entry Point



def _read_data(filename):                                                             # Lee el archivo CSV y lo devuelve como DataFrame
  logger.info('Reading file {}'.format(filename))
  return pd.read_csv(filename)                                                        # Retornamos el resultado (DataFrame) de leer el CSV usando la libreria Pandas como "pd"



def _extract_newspaper_uid(filename):                                                 # Retorna el UID de la noticia (nombre del periodico) dentro del CSV
  logger.info('Extracting newspaper uid')
  newspaper_uid = filename.split('_')[0]                                              # Obtenemos el UID del nombre de nuestro archivo (Le dimos el formato que comenzara el con su nombre Ej, "elpais_something") y lo obtenemos con el método ".split('_')"
  logger.info('Newspaper uid detected: {}'.format(newspaper_uid))
  return newspaper_uid                                                                # Retornamos el UID (el nombre del periodico)



def _add_newspaper_uid_column(df, newspaper_uid):                                     # Agrega una columna al DataFrame con el valor del UID del periodico          
  logger.info('Filling newspaper_uid column with {}'.format(newspaper_uid))
  df['newspaper_uid'] = newspaper_uid                                                 # Creamos una columna llamada 'newspaper_uid' y le agregamos el valor que obtuvimos para que lo podamos aplicar a cualquier DataSet
  return df                                                                           # Retornamos el DataFrame modificado



def _extract_host(df):                                                                # Extrae el Host de las URLs y crea una columna llamada 'host' y llena los valores de sus celdas
  logging.info('Extracting host form urls')
  df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)                      # Creamos la columna 'host' y los valores los obtenemos usando el método ".apply" que saca de la columna 'url' el nombre del host, usa como parámetro una función lambda que usa la 'url' para parsear el 'host' con el método 'urlparse(url).netloc', la propiedad "netloc" es en realidad el 'host
  return df                                                                           # retornamos el DataFrame modificado



if __name__ == '__main__':                                                            # Este script automatiza (como crear recetas) para la Transformación de datos paso a paso a cualquier dataset de nociticias para que quede limpio
  parser = argparse.ArgumentParser()                                                  # Le preguntamos al usuario cual va a ser el archivo con el que vamos a trabajar usando ".ArgumentParser()"
  parser.add_argument('filename', help='The path to the dirty data', type=str)        # Le añadimos un argumento al cual llameremos 'filename' y le agregamos un texto de ayuda 'help' (mensaje que aparecerá cuando usemos comando -h, --help) y le decimo que lo que nos regresará el usuario es un string
  arguments = parser.parse_args()                                                     # Parseamos los argumentos con el método ".parse_args()" viene de libreria y los guardamos en la variable "arguments"            

  df = main(arguments.filename)                                                       # Invocamos a la función main(arguments.filename) y le mandamos como argumento el "arguments.filename", y lo guardamos como nuestro DataFrame final
  print(df)                                                                           # Mostramos la información