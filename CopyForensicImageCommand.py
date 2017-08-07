import Comandos
import model
import util
import threading
import shutil
import pprint
import os
import time


class CopyForensicImageThread(threading.Thread):
    def __init__(self, caseName, idCase, alias, files, incomingFolder, destinationFolder):
        threading.Thread.__init__(self)
        self.caseName = caseName
        self.idCase = idCase
        self.alias = alias
        self.files = files
        self.incomingFolder = incomingFolder
        self.destinationFolder = destinationFolder

    def run(self):
        copy = CopyForensicImageCommand(self.caseName, self.idCase, self.alias, self.files, self.incomingFolder,
                                        self.destinationFolder)
        copy.execute()


class CopyForensicImageCommand:
    def __init__(self, caseName, idCase, alias, files, incomingFolder, destinationFolder):
        self.caseName = caseName
        self.idCase = idCase
        self.alias = alias
        self.files = files
        self.incomingFolder = incomingFolder
        self.destinationFolder = destinationFolder

    def execute(self):
        # Copiar datos de carpeta incoming a carpeta destino con integridad de datos

        # Para verificar la integridad se cogera cada fichero y se le calculara el md5. Cuando se copie al destino se calculara
        # tambien el md5 para verificar que la copia se ha realizado correctamente

        Comandos.log.info('Copy files')

        # Filtrar todos los ficheros que hay en incoming para quedarse solo con los que se necesitan copiar (estan en files)
        incomingFiles = os.listdir(self.incomingFolder)
        if self.files != None:
            incomingFilesFiltered = list(filter(lambda f: f in self.files, incomingFiles))
        else:
            incomingFilesFiltered = incomingFiles

        # Si no hay ficheros que copiar el proceso ha finalizado
        if len(incomingFilesFiltered) == 0:
            Comandos.log.info('No files to process')
            return

        # Crear carpeta destino si no existe
        util.create_folder_if_not_exist(self.destinationFolder)

        # Copiar solo los ficheros filtrados
        incomingFilesFullPath = list()
        for file in incomingFilesFiltered:
            incomingFile = self.incomingFolder + os.sep + file
            shutil.copy2(incomingFile, self.destinationFolder)
            Comandos.log.info('Copy file ' + incomingFile + ' to ' + self.destinationFolder)
            incomingFilesFullPath.append(incomingFile)

        # Calcular el hash de cada fichero origen, de cada fichero destino y verificar que son el mismo para verificar integridad

        # Recuperar los nombres de fichero originales
        Comandos.log.info('Files: ' + str(incomingFilesFiltered))

        # Lista donde se guardaran todos los ficheros pertenecientes al caso, todos con los mismos atributos CASE, ID y ALIAS
        forensicCase = list()

        for incomingFile in incomingFilesFullPath:
            destinationFile = self.destinationFolder + os.sep + util.get_basename(incomingFile)

            md5IncomingFile = util.get_md5(incomingFile)
            md5DestinationFile = util.get_md5(destinationFile)

            if md5IncomingFile != md5DestinationFile:
                Comandos.log.error('Error: integrity error file ' + incomingFile)
                print('Error: integrity error file ' + incomingFile)
                return

            # Recuperar datos del fichero copiado
            dataFile = os.stat(destinationFile)

            fileCase = model.FileCase(
                caseName=self.caseName,
                idCase=self.idCase,
                alias=self.alias,
                size=util.get_bytes_in_megabytes(dataFile.st_size),
                fileName=util.get_basename(destinationFile),
                hashMd5=md5DestinationFile,
                # Fecha de creacion del fichero original
                creationTime=util.format_date_time(time.ctime(os.stat(incomingFile).st_ctime)),
                # Fecha de creacion del fichero copiado
                copyTime=util.format_date_time(time.ctime(dataFile.st_ctime)),
                fileType=util.get_extension(destinationFile)
            )

            forensicCase.append(fileCase)

        Comandos.log.debug('Copy files to destination finished')

        # TODO se podran eliminar los antiguos una vez copiados?


        Comandos.log.debug("Registers: " + pprint.pformat(forensicCase))

        # Conectar a bbdd, creando la tabla "filecase" si no existe, y guardar todos los casos
        Comandos.log.info('Inserting metadata in database: %s', forensicCase)

        try:
            model.db.connect()
            model.db.create_table(model.FileCase, safe=True)
            with model.db.transaction():
                [fileCase.save(force_insert=True) for fileCase in forensicCase]
        except:
            Comandos.log.error('Database error, aborting operation')
            return
        finally:
            model.db.close()

        Comandos.log.info('Metadata inserted in database')

        # Guardar los ficheros en un fichero de texto con campos separados por |
        Comandos.log.info('Creating CSV file')
        csv = [fileCase.get_text_format() for fileCase in forensicCase]

        # Poner cada fichero del caso en una linea distinta y guardar en fichero
        # El nombre de fichero sera la composicion de caso, id y alias y con extension csv
        csvContent = util.join_list('\n', csv)
        csvName = self.caseName + '_' + str(self.idCase) + '_' + self.alias + '.csv'
        csvFile = open(csvName, 'w')
        csvFile.write(csvContent)
        csvFile.close()
        Comandos.log.info('CSV file created')
        Comandos.log.info('Copy finished')
