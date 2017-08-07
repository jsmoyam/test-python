import Comandos
import util


class ShellCommand:
    def __init__(self, command):
        self.command = command

    def execute(self):
        # Ejecutar un comando shell del sistema operativo

        Comandos.log.info('Execute shell command')

        (output, err) = util.execute_shell(util.join_list(' ', self.command))
        print(output)

        Comandos.log.info('Execute shell command finished')
