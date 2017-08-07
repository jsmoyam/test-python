# Fichero de utilidades

import hashlib
import os
import shlex
import datetime


# Calcula el md5 de un fichero
def get_md5(fileName): return hashlib.md5(open(fileName, 'rb').read()).hexdigest()


# Devuelve el basename de un fichero con su ruta completa
def get_basename(fileName): return os.path.basename(fileName)


# Devuelve la extension de un fichero
def get_extension(fileName): return os.path.splitext(fileName)[1][1:]


# Convierte de bytes a megabytes redondeando a dos decimales
def get_bytes_in_megabytes(bytes): return "%.2f" % (bytes / (1024 * 1024))


# Recupera fecha de creacion de fichero en segundos desde 1970
def get_creation_time(fileName): return os.stat(fileName).st_ctime


# Formatea una fecha en formato ctime a YYYY-MM-DD HH:MM:SS
def format_date_time(value): return datetime.datetime.strptime(value, '%a %b %d %H:%M:%S %Y')


# Une todas las representaciones string de una lista con un delimitador
def join_list(sep, list_): return sep.join(map(str, list_))


# Split respetando comillas dobles
def split_with_quotes(value):
    lex = shlex.shlex(value)
    lex.quotes = '"'
    lex.whitespace_split = True
    lex.commenters = ''
    return list(lex)
