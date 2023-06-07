import yaml                                                               # Importamos la librería "yaml" en virtual env (conda install yaml)

__config = None                                                           # Variable global, nos va a servir para poder "cachear" nuestra configuración

def config():                                                             # Retorna un diccionario, recibe el archivo como parámetro (más abajo)
  global __config
  if not __config:                                                        # Solo vamos a leer la configuracion una sola vez, y si ya esta cargada solo la devolvemos y si no esta cargada la abrimos y enviamos
    with open('config.yaml', mode='r') as file:                           # Abrimos el archivo config.yaml
      __config = yaml.load(file, Loader=yaml.FullLoader)                  # Guardamos el archivo a "__config", funcion retorna un diccionario
      #__config = yaml.safe_load(file)
  return __config                                                         # Retornamos nuestra configuracion