import argparse
import logging
import news_page_object as news
from common import config  # Importamos la funcion "config" del modulo "common.py"
logging.basicConfig(level=logging.INFO)




logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Beginning scraper for {}'.format(host))
    homepage = news.HomePage(news_site_uid, host)

    for link in homepage.article_links:
        print(link)


if __name__ == '__main__':   # Entry Point
    parser = argparse.ArgumentParser() # Instanciamos un objetod de la clase ArgumentoParser

    news_site_choices = list(config()['news_sites'].keys()) # Nos regresa un iterador lo convertimos en una lista
    parser.add_argument('news_site',                             # Añadimos varias opciones
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_site_choices) # Las opciones que estan en "config.yaml" 
    args = parser.parse_args()
    _news_scraper(args.news_site)     