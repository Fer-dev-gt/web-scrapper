# Este archivo sirve para iniciar los objetos e implementar las librerias que nos permitiran cargar nuestro DataSet en una Data Bae

from sqlalchemy import create_engine                                              # Importamos 'create_engine' de la libreriá 'sqlalchemy', hay que instalarlo en consolo/virtual env usando "conda install sqlalchemy"
from sqlalchemy.orm import sessionmaker                                           # Importamos el 'sessionmaket' de la libreria 'sqlalchemy.orm', ORM lo habilitmos en la siguiente linea de abajo (ORM = Object Relational Mapper)
from sqlalchemy.ext.declarative import declarative_base                           # Nos permite tener acceso a las funcionalida de ORM (Object Relational Mapper) que nos permite trabajar con objetos de Python en vez de SQL directamente


# Declaramos 3 variables usando las librerías que importamos

engine = create_engine('sqlite:///newspapers.db')                                 # Acá le digo a 'sqlalchemy' que quiero utlizar 'sqllite', ya viene instalado dentro de la distribución de Python, y le paso como parámetro el nombre que tendra el archivo de la base de datos
Session = sessionmaker(bind=engine)                                               # Generamos el Objeto 'session/sessionmaker' y le pasamos como parámetro directamente nuestra variable del motor ('bind=engine')
Base = declarative_base()                                                         # Generamos nuestra "clase base", la guardamos en una variable de la cual van a extender todos nuestro modelos

