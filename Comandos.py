# Instalacion por pip: peewee, terminaltables

import cmd
import os
import shlex
import logging
import logging.handlers
import util
import CopyForensicImageCommand
import ListIncomingCommand
import ListCommand
import MmlsCommand
import ShellCommand

# Variables que el interprete tiene definidas
VARIABLES = {'INCOMING_FOLDER': 'INCOMING_FOLDER', 'DESTINATION_FOLDER': 'DESTINATION_FOLDER'}


# Definicion del log
def getLog(logfile):
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)

    # Formatter especifico
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Añadir dos handler: fichero y consola
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(fh)
    # log.addHandler(ch)

    return log


# Ejecutar log
log = getLog('output.log')


# Clase principal de ejecucion
class Comandos(cmd.Cmd):
    """Interprete de comandos"""
    prompt = "OneSecurity> "
    intro = "Command interpreter"
    doc_header = "Available commands"
    undoc_header = "Not documented commands"
    misc_header = "Other methods"
    ruler = "-"

    def do_set(self, args):
        """Set environment variables INCOMING_FOLDER and DESTINATION_FOLDER:
            set INCOMING_FOLDER /var/incoming
            set DESTINATION_FOLDER /var/copy"""

        # Parsear comando teniendo en cuenta comillas simples y dobles: copy "hola mundo" 22 mi_alias
        argsList = shlex.split(args)
        if len(argsList) != 2:
            print('Not enough arguments')
        # Detectar que las variables son correctas. Solo se permiten las definidas en el diccionario global
        elif argsList[0] not in VARIABLES.keys():
            print('Error: variable ' + argsList[0] + ' not defined in the system')
        else:
            # Asignar como atributo de clase, previendo que no acabe nunca con el separador del sistema operativo
            value = str(argsList[1])
            if value.endswith(os.sep):
                value = value[:-1]

            setattr(self, argsList[0], value)
            print('Command sucessful')

    def do_get(self, args):
        """Get environment variables INCOMING_FOLDER and DESTINATION_FOLDER:
            get INCOMING_FOLDER
            get DESTINATION_FOLDER"""

        # Parsear comando teniendo en cuenta comillas simples y dobles: copy "hola mundo" 22 mi_alias
        argsList = shlex.split(args)
        if len(argsList) != 1:
            print('Not enough arguments')
        # Detectar que las variables son correctas. Solo se permiten las definidas en el diccionario global
        elif argsList[0] not in VARIABLES.keys():
            print('Error: variable ' + argsList[0] + ' not defined in the system')
        else:
            print(getattr(self, argsList[0]))
            print('Command sucessful')

    def do_copy(self, args):
        """Copy forensic images from incoming folder and insert metadata in database and csv file. Not blocking operation
           Arguments: caseName idCase alias [[file1],[file2]...]
           Examples:
               copy test_case 22 my_alias file1,file2,file3
               copy "test case" 22 'my alias'"""

        # Parsear comando teniendo en cuenta comillas simples y dobles: copy "hola mundo" 22 mi_alias
        argsList = shlex.split(args)

        files = None
        if len(argsList) < 3 or len(argsList) > 4:
            print('Not enough arguments')
        else:
            # Detectar que el argumento id es numerico
            try:
                int(argsList[1])
            except:
                print('Error: idCase must be numeric')
                return

            # Detectar que estan definidas las variables INCOMING_FOLDER y DESTINATION_FOLDER
            if not hasattr(self, VARIABLES.get('INCOMING_FOLDER')) or not hasattr(self,
                                                                                  VARIABLES.get('DESTINATION_FOLDER')):
                print('Variables INCOMING_FOLDER and DESTINATION_FOLDER must exist. Please set before copy')
                return

            # Recuperar argumento de lista de ficheros a procesar
            if len(argsList) == 4:
                files = argsList[3]

            thread = CopyForensicImageCommand.CopyForensicImageThread(argsList[0], int(argsList[1]), argsList[2], files,
                                                                      getattr(self, VARIABLES.get('INCOMING_FOLDER')),
                                                                      getattr(self,
                                                                              VARIABLES.get('DESTINATION_FOLDER')))
            thread.start()
            print('Command executing in background')

    def do_list_incoming(self, args):
        """List incoming folder files"""

        if len(args) != 0:
            print('This command has no arguments')
            return

        # Detectar que esta definida la variable INCOMING_FOLDER
        if not hasattr(self, VARIABLES.get('INCOMING_FOLDER')):
            print('Variable INCOMING_FOLDER must exist. Please set before copy')
            return

        ListIncomingCommand.ListIncomingCommand(getattr(self, VARIABLES.get('INCOMING_FOLDER'))).execute()
        print('Command sucessful')

    def do_list(self, args):
        """List all metadata from database with filters"""

        argsList = util.split_with_quotes(args)
        ListCommand.ListCommand(argsList).execute()
        print('Command sucessful')

    def do_mmls(self, args):
        """Execute mmls over copied file: mmls file.E01"""

        argsList = util.split_with_quotes(args)
        if len(argsList) != 1:
            print('Syntax error')
            return

        # Detectar que esta definida la variable DESTINATION_FOLDER
        if not hasattr(self, VARIABLES.get('DESTINATION_FOLDER')):
            print('Variable DESTINATION_FOLDER must exist. Please set before copy')
            return

        MmlsCommand.MmlsCommand(getattr(self, VARIABLES.get('DESTINATION_FOLDER')), argsList[0]).execute()
        print('Command sucessful')

    def do_shell(self, args):
        """Execute shell command: ls -la"""

        argsList = util.split_with_quotes(args)
        ShellCommand.ShellCommand(argsList).execute()
        print('Command sucessful')

    def do_run(self, args):
        """Execute script with commands: run script.one"""

        try:
            # Leer fichero en una lista
            commands = util.read_file(args)

            # Eliminar lineas vacias del fichero
            commands = [x for x in commands if x]

            # Ejecutar todos los comandos
            for command in commands:
                print('Execute ' + command)
                interpreter.onecmd(command)

            print('Command sucessful')
        except:
            print('File error: ' + args)

    def do_exit(self, args):
        """Exit from interpreter"""
        print('See you soon!')
        return True

    def emptyline(self):
        """No operation"""
        pass


if __name__ == '__main__':
    interpreter = Comandos()
    # interpreter.onecmd('set INCOMING_FOLDER /vagrant/files')
    # interpreter.onecmd('set DESTINATION_FOLDER /home/juan/tmp')
    # interpreter.onecmd('list_incoming')
    # interpreter.onecmd('copy 1 1 1')
    # interpreter.onecmd('copy 1 1 1 cfreds_2015_data_leakage_rm#2.E01')
    # interpreter.onecmd('copy 2 2 2 cfreds_2015_data_leakage_rm#2.E01')
    # interpreter.onecmd('list')
    # interpreter.onecmd('list caseName like "2" and idCase==2')
    # interpreter.onecmd('list caseName like "2" and idCase==2 order by copyTime desc')
    # interpreter.onecmd('list caseName like "2" and idCase==2 and copyTime < "2017-08-07 00:14:00"')
    # interpreter.onecmd('mmls ')
    # interpreter.onecmd('mmls cfreds_2015_data_leakage_rm#2.E01')
    # interpreter.onecmd('shell ls -la')
    # interpreter.onecmd('run script.one')
    interpreter.cmdloop()
