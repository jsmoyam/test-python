import Comandos
import util
import os


class ListIncomingCommand:
    def __init__(self, incomingFolder):
        self.incomingFolder = incomingFolder

    def execute(self):
        # Listar el contenido de la carpeta incoming

        Comandos.log.info('List incoming files')

        incomingFiles = os.listdir(self.incomingFolder)
        print(util.join_list('\n', incomingFiles))

        Comandos.log.info('List finished')
