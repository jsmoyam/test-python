from peewee import *
import util
import terminaltables

db = SqliteDatabase('cases.db')


# Modelo de base de datos para guardar un caso
class FileCase(Model):
    # Campos de la base de datos
    caseName = TextField()
    idCase = IntegerField()
    alias = TextField()
    size = FloatField()
    fileName = TextField()
    hashMd5 = TextField()
    creationTime = DateTimeField()
    copyTime = DateTimeField()
    fileType = TextField()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return util.join_list('; ', self.get_list_format())

    def get_list_format(self):
        output = list()
        output.append(self.caseName)
        output.append(self.idCase)
        output.append(self.alias)
        output.append(self.size)
        output.append(self.fileName)
        output.append(self.hashMd5)
        output.append(self.creationTime)
        output.append(self.copyTime)
        output.append(self.fileType)
        return output

    # Devuelve el objeto en formato csv con separador '|'
    def get_text_format(self):
        return util.join_list('|', self.get_list_format())

    # Devuelve una lista con los datos representados en forma de tabla para su representacion en consola
    def _get_table_data(self):
        tableList = list()
        header = ['caseName', 'idCase', 'alias', 'size', 'fileName', 'hashMd5', 'creationTime', 'copyTime', 'fileType']
        tableList.append(header)
        tableList.append(self.get_list_format())
        table = terminaltables.AsciiTable(tableList)
        return table.table

    class Meta:
        database = db


def get_table(fileCases):
    # Tabla con los resultados tabulados
    tableList = list()

    # Se añade en primer lugar la cabecera
    header = ['caseName', 'idCase', 'alias', 'size', 'fileName', 'hashMd5', 'creationTime', 'copyTime', 'fileType']
    tableList.append(header)

    # Se van añadiendo las filas de cada uno de los registros
    for fileCase in fileCases:
        tableList.append(fileCase.get_list_format())

    table = terminaltables.AsciiTable(tableList)
    return table.table
