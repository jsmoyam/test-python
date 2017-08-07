import os
import Comandos
import util


class MmlsCommand:
    def __init__(self, destination_folder, file_name):
        self.destination_folder = destination_folder
        self.file_name = file_name

    def execute(self):
        # Ejecutar el comando mmls sobre un fichero

        Comandos.log.info('Execute mmls')

        destination_file = self.destination_folder + os.sep + util.get_basename(self.file_name)
        command = ['mmls']
        command.append(destination_file)
        (output, err) = util.execute_shell(util.join_list(' ', command))
        print(output)

        Comandos.log.info('Mmls finished')
