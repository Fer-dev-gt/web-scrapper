from sqlalchemy import Column, String, Integer                                # Nos traemos de la libreria 'sqlalchemy' la 'Column, String e Integer'
from base import Base                                                         # Del archivo 'base.py' nos traemos nuestra Clase 'Base'

class Article(Base):                                                          # Declaramos nuestra clase Article que extiende de la clase Base
  __tablename__ = 'articles'                                                  # Le decimos como se va a llamar nuestra tabla
  id = Column(String, primary_key=True)                                       # Declaramos nuestra estructura de datos, todos los datos que recolectamos en nuestro CSV los estamos esctructurando para nuestra Base de Datos
  body = Column(String)                                                       # La mayoria de los datos con los que trabajamos son de tipo String
  host = Column(String)
  title = Column(String)
  newspaper_uid = Column(String)
  n_tokens_body = Column(Integer)                                             # Pero tambien podemos usar tipo Integer entre otros
  n_tokens_title = Column(Integer)                                            # Le pusimos tipo Integer a los tokens porque tienen que ser números enteros, no podemos tener medio token (media palabra)
  url = Column(String, unique=True)

  # Generamos nuestra inicialización del Objeto, nos traemos las variables de arriba y se las asiganmos a nuestras variables de instancia
  def __init__(self, uid, body, host, title, newspaper_uid, n_tokens_body, n_tokens_title, url): 
    self.id = uid
    self.body = body
    self.host = host
    self.title = title
    self.newspaper_uid = newspaper_uid
    self.n_tokens_body = n_tokens_body
    self.n_tokens_title = n_tokens_title
    self.url = url