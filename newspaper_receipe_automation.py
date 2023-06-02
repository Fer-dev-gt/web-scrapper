import pandas as pd
import argparse                                                                       # Librería para convertir esto en un Script
import hashlib                                                                        # La librería hashlib nos sirve para trabajar con operacione criptograficas y para generar un hash de la URL
import re
import nltk
from   nltk.corpus import stopwords                                                   # Los 'Stowords' son palabras que no nos aportan información revelante, Ej: 'el', 'la', 'y' etc. que se usan mucho en nuestro idioma pero que no sirver para determinar que sucede en nuestro texto

import logging
from urllib.parse import urlparse
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)                                                  # Obtenemos una refencia de nuestro Logger con ".getLogger(__name__)" con el nombre interno que tiene nuestro archivo


def main(filename):                                                                   # Ejecuta las funciones que limpian y transforman a nuestro DataFrame el cual retornamos, Recibe como argumento al "filename" que habiemos creado como argumento en el Entry Point
  logger.info('Starting cleaning process 🧹')
  df = _read_data(filename)                                                           # Leemos los datos y creamos un DataFrame con este función, 'df' significa DataFrame
  newspaper_uid = _extract_newspaper_uid(filename)                                    # Guardamos y extraemos el UID (nombre del periodico) de los articulos de noticias, pasamos el archivo CSV
  df = _add_newspaper_uid_column(df, newspaper_uid)                                   # Modificamos el DataFrame en las columnas le añadimos el UID, recibe 2 parámetros, el DataFrama "df" como lo llevamos trabajando y el valor del UID al cual lo meteremos en el DataFrame
  df = _extract_host(df)                                                              # Extraemos el 'host' del DataFrame (Ej: elpais.com) y lo agregamos como nueva columnas, enviamos el DataFrame
  df = _fill_missing_titles(df)                                                       # Llenamos los "missign titles" de las noticias, estos aparecen como NaN y extraemos el titulo de la URL y lo colocamos en el DataFrame
  df = _generate_uids_for_rows(df)                                                    # Genera un 'hash' que sera el "uid" de cada articulo de noticia
  df = _remove_news_lines_from_body(df)                                               # Remueve los caracteres y simbolos indicados
  df = _tokenize_column(df, 'title')                                                  # Creamos nuestra columna 'n_tokens_title' y le pasamos los datos de los token encontrados y los insertamos en el DataFrame, mandamos como parámetro el DataFrame y el nombre de la columna para agregar
  df = _tokenize_column(df, 'body')                                                   # Hacemos lo mismo pero para el body
  return df                                                                           # Regresamos el DataFrame "Transformado" al Entry Point



def _read_data(filename):                                                             # Lee el archivo CSV y lo devuelve como DataFrame
  logger.info('Reading file {} 🤓'.format(filename))
  return pd.read_csv(filename)                                                        # Retornamos el resultado (DataFrame) de leer el CSV usando la libreria Pandas como "pd"



def _extract_newspaper_uid(filename):                                                 # Retorna el UID de la noticia (nombre del periodico) dentro del CSV
  logger.info('Extracting newspaper uid 💉')
  newspaper_uid = filename.split('_')[0]                                              # Obtenemos el UID del nombre de nuestro archivo (Le dimos el formato que comenzara el con su nombre Ej, "elpais_something") y lo obtenemos con el método ".split('_')"
  logger.info('Newspaper uid detected: {} 🕵🏽‍♂️'.format(newspaper_uid))
  return newspaper_uid                                                                # Retornamos el UID (el nombre del periodico)



def _add_newspaper_uid_column(df, newspaper_uid):                                     # Agrega una columna al DataFrame con el valor del UID del periodico          
  logger.info('Filling newspaper_uid column with {} ⛽️'.format(newspaper_uid))
  df['newspaper_uid'] = newspaper_uid                                                 # Creamos una columna llamada 'newspaper_uid' y le agregamos el valor que obtuvimos para que lo podamos aplicar a cualquier DataSet
  return df                                                                           # Retornamos el DataFrame modificado



def _extract_host(df):                                                                # Extrae el Host de las URLs y crea una columna llamada 'host' y llena los valores de sus celdas
  logger.info('Extracting host form urls 👽')
  df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)                      # Creamos la columna 'host' y los valores los obtenemos usando el método ".apply" que saca de la columna 'url' el nombre del host, usa como parámetro una función lambda que usa la 'url' para parsear el 'host' con el método 'urlparse(url).netloc', la propiedad "netloc" es en realidad el 'host
  return df                                                                           # retornamos el DataFrame modificado



def _fill_missing_titles(df):                                                         # Extraemos el titulo de la URL y lo colocamos en el DataFrame a las noticias que no tienen titulo
  logger.info('Filling missing titles 🗂️')
  missing_titles_mask = df['title'].isna()                                            # Generamos nuestra mascara Booleana para identificar donde estan los datos faltantes seleccionando la columna 'title' y usando el método ".isna()"        
  missig_titles = (df[missing_titles_mask]['url']                                     # Extramos el titulo de la columna 'url' con los valores que faltan guaradados en 'missing_title_mask' y le aplicamos varias transformaciones para que tenga el formato adecuado
                  .str.extract(r'(?P<missing_titles>[^/]+)$')                         # Usando Expresiones Regulares (le decimos que selecciones todo menos las diagonales, queremos que haya uno o más y nos vamos hasta el final de nuestro string)y dandole un nombre al grupo de coincidencias "missing_titles" usamos el método ".str.extract()"
                  .applymap(lambda title: title.replace('-', ' '))                    # Reemplazamos las diagonales que viened de la URL y los reemplazamos por espacios usando el método de Pandas ".applymap()"
                  .applymap(lambda final_title: final_title.capitalize()))            # Por ultimo hacemos que las noticias empiezen con mayuscula para que tenga el mismo formato que el resto de noticias
  df.loc[missing_titles_mask, 'title'] = missig_titles.loc[:, 'missing_titles']       # Asignamos los titulos extraidos a una columna llamada usando la notación ".loc[]", le decimos que seleccionas todas las filas donde hay 'missing titles' y queremos la columna 'title'. Despues del '=' le pasamos todos nuestros 'missing_titles' con ':' y le pasamos la columna 'missing_titles' que es el nombre que le dimos a nuestro grupo en las Expresiones Regulares
  return df                                                                           # Regresamos nuestro DataFrame actualizado



def _generate_uids_for_rows(df):                                                      # Genera un uid para cada fila usando "hashes", estos uid reemplazara al indice de fila que viene por defecto
  logger.info('Generating uids fo each row 🪪')
  uids = (df.apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)       # Generamos nuestros "hashes" usando haslib.md5 (no es recomendado por fallos de seguridad) cuando queremos trabajar con las filas usamos "axis=1". Generamos un array de bytes y un f8 por defecto
            .apply(lambda hash_object: hash_object.hexdigest())                       # Convertimos los datos a una representación hexadecimal usando el método "hexdigest()"   
          )
  df['uid'] = uids                                                                    # Añadimos los hashes a la columna 'uid'
  df.set_index('uid', inplace=True)                                                   # Le decimos que queremos a la columna 'uid' como index de las filas, "implace=True" hace que modifiquemos directamente nuestro DataFrame en vez de generar uno nuevo
  return df



def _remove_news_lines_from_body(df):                                                 # Elimina de la seccion de 'body' los saltos de linea (\n) los borra y reformatea el titulos para que este presentable
  logger.info('Remove new lines from body 🧑🏽‍💻')
  stripped_body = (df.apply(lambda row: row['body'], axis=1)                          # Obtenemos el 'body' de cada fila con "axis=1"
                    .apply(lambda body: re.sub(r'(\n|\r)+',r'', body))                # Usando Expresiones regulares eliminamos el simbolo "\n" y "\r" del 'body'
                  )
  df['body'] = stripped_body                                                          # Agregamos los nuevos valores a la columna "body"
  return df



def _tokenize_column(df, column_name):                                                 # Retorna los datos que iran en "n_tokens_title" que seran el número de palabras dentro del titulo que son significativas, no se cuentas palabras como "la, el, y, o"
  logger.info('Calculating the number of unique tokens in {} 🔐'.format(column_name))
  stop_words = set(stopwords.words('spanish'))                                         # Definimos cuales serán nuestro 'Stopwords' dentro de un Set y le decimos que los queremos en Español

  n_tokens = (df.dropna()                                                              # Primero eliminamos cualquier dato que sea un NaN, todo el resultado de las transformaciones las guardamos en la variable "n_tokens"
            .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)           # Tokenizamos las filas con "axis=1" y ".word_tokenize()"
            .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens))) # Eliminamos todas aquellas palabras que no sean Alfanumericas, lo hacemos aplicando un ".filter()" y ".isalpha()", nos regresa un iterados asi que lo pasamos a una lista
            .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))      # Convertimos todos los tokens a lowercase, pasamos el resultado de objeto a una lista
            .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list))) # Eliminamos a todas las palabras que sean Stopwords, osea las que esten guardadas en "word_list"
            .apply(lambda valid_word_list: len(valid_word_list))                       # No queremos en si la lista de palabras, si no su longitud, asi que calculamos la longitud de cada lista
            )
  df['n_tokens_{}'.format(column_name)] = n_tokens                                     # Colocamos la cantidad de token encontrados en la columna correspondiente
  return df




if __name__ == '__main__':                                                            # Este script automatiza (como crear recetas) para la Transformación de datos paso a paso a cualquier dataset de nociticias para que quede limpio
  nltk.download('punkt')                                                              # Nos da la libreria para poder "tokenizar" es decir dividir palabras
  nltk.download('stopwords')
  parser = argparse.ArgumentParser()                                                  # Le preguntamos al usuario cual va a ser el archivo con el que vamos a trabajar usando ".ArgumentParser()"
  parser.add_argument('filename', help='The path to the dirty data', type=str)        # Le añadimos un argumento al cual llameremos 'filename' y le agregamos un texto de ayuda 'help' (mensaje que aparecerá cuando usemos comando -h, --help) y le decimo que lo que nos regresará el usuario es un string
  arguments = parser.parse_args()                                                     # Parseamos los argumentos con el método ".parse_args()" viene de libreria y los guardamos en la variable "arguments"            

  df = main(arguments.filename)                                                       # Invocamos a la función main(arguments.filename) y le mandamos como argumento el "arguments.filename", y lo guardamos como nuestro DataFrame final
  print(df)                                                                           # Mostramos la información
  #df.to_csv('eluniversal_limpio.csv', encoding="utf-8", sep = ';')                   # Para crear un CSV con los datos finales y limpiados