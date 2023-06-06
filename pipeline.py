# Programa que automatiza el proceso ETL (extracción de noticias de periodicos, su limpiamiento y carga a base de datos)

import subprocess                                                           # Importamos 'subprecess' que es parte de la librería estandar de Python, que nos permite manipular directamente archivos de Terminal, es como si tuvieramos la terminal directamente en Python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

news_sites_uids = ['eluniversal', 'elpais', 'cnbc']                         # Creamos una lista con los nombres de los sitios de noticias a los cuales vamos a extraer los articulos de noticias (estan declarados en config.yaml)

def main():                                                                 # Nuestra función main se encarga de todos los procesos de ETL de nuestro 'web scrapper' desde consultar las noticias hasta subir los articulos a la base de datos
  _extract()
  _transform()
  _load()



def _extract():
  logger.info('Starting extract process')
  for news_site_uid in news_sites_uids:                                     # Iteramos por cada  periodico dentro de los 'news_sites_uids'
    subprocess.run(['python', 'main.py', news_site_uid], cwd='./extract')   # Corremos un 'Subproceso' (que es definir en Python lo que ya hemos hecho) usando "subprecess.run([instrucciones de que programa correr])". Le decimos que ejecuto el archivo de Python 'main.py' con los parámetros de 'news_site_uid' (el periodico en especico) del archivo que se encuentra en la carpeta 'cwd='./extract'' (cwd significa "Current Working Directory") 
    subprocess.run(['find', '.', '-name', '{}*'.format(news_site_uid), '-exec', 'mv', '{}', '../transform/{}_.csv'.format(news_site_uid), ';'], cwd='./extract')    # Movemos los archivos que se generaron usando 'find' con los archivos que tiene de nombre cierto patron que tengan "*(lo que sea).format(news_site_uid)" y que los mueva (usando 'mv') a la carpeta '../transform' y les cambiamos el nombre al formato indicado




def _transform():
  logger.info('Starting transform process')
  for news_site_uid in news_sites_uids:                                     
    dirty_data_filename = '{}_.csv'.format(news_site_uid)                                                   # Guardamos el archivo que movimos en la parte de 'extract' y lo guardamos en la variable 'dirty_data_filename'
    clean_data_filename = 'clean_{}'.format(dirty_data_filename)                                            # Le cambiemos el nombre al archivo para que indique que ya fue limpiado
    subprocess.run(['python', 'main.py', dirty_data_filename], cwd='./transform')                           # Ejecutamos el subproceso para que ejecute la función main del folder de 'transform' y le pasamos como parametro el archivo sucio 'dirty_data_filename' y que lo ejecute en el directorio "cwd=./transform"
    subprocess.run(['rm', dirty_data_filename], cwd='./transform')                                          # Eliminamos el archivo sucio usando 'rm' (remove), lo ejecutamos en el directorio "cwd=./transform"
    subprocess.run(['mv', clean_data_filename, '../load/{}.csv'.format(news_site_uid)], cwd='./transform')  # Movemos nuestro archivo limpio a la carpeta de "./load" para despues subirlo a nuestra base de datos con el nombre del periodico.csv y que lo ejecute en el directorio "cwd=./transform"



def _load():
  logger.info('Starting load process')
  for news_site_uid in news_sites_uids:
    clean_data_filename = '{}.csv'.format(news_site_uid)                          # Declaramos en nombre del archivo limpio
    subprocess.run(['python', 'main.py', clean_data_filename], cwd='./load')      # Ejecutamos el archivo main de la carpeta "./load" para subir el archivo que le enviamos como parámetro ("clean_data_filename") a la base de datos, lo ejecutamos en el directorio "cwd=./load"
    subprocess.run(['rm', clean_data_filename], cwd='./load')                     # Eliminamos el archivo limpio (ya que ya se encuentra en la base de datos) usando 'rm' (remove), lo ejecutamos en el directorio "cwd=./load"       




if __name__ == '__main__':                                                        # Entry Point principal de todo y simple que no recibe parametros
  main()