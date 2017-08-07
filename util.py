# Fichero de utilidades

import hashlib
import os, os.path
import shlex
import datetime
import subprocess

# Calcula el md5 de un fichero
def get_md5(fileName):
    # Esta forma da errores de memoria al intentar cargar ficheros muy grandes
    # return hashlib.md5(open(fileName, 'rb').read()).hexdigest()

    # Es mejor hacer el hash por pasos aprovechandose de que cada chunk interno de md5 es de 128 bytes
    read_size = 1024
    checksum = hashlib.md5()
    with open(fileName, 'rb') as f:
        data = f.read(read_size)
        while data:
            checksum.update(data)
            data = f.read(read_size)
    checksum = checksum.hexdigest()
    return checksum


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


# Ejecutar un comando del sistema operativo devolviendo su salida y errorlevel
def execute_shell(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = list()
    for line in p.stdout.readlines():
        output.append(line.strip().decode('utf-8'))
    retval = p.wait()

    return join_list('\n', output), retval


# Lee un fichero de texto devolviendo sus lineas en una lista
def read_file(file_name):
    with open(file_name) as f:
        lines = f.read().split('\n')
    return lines


# Crea un directorio. Si ya existe no hace nada
def create_folder_if_not_exist(folder):
    if not os.path.exists(folder): os.makedirs(folder)
