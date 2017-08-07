import Comandos
import util
import model


class ListCommand:
    def __init__(self, filter):
        self.filter = filter

    def execute(self):
        # Listar los metadatos en funcion de filtros (caseName==1 and idCase==1)

        Comandos.log.info('List metadata')

        # Buscar en la base de datos en funcion del filtro
        output = list()
        try:
            model.db.create_table(model.FileCase, safe=True)
            if len(self.filter) == 0:
                query = model.FileCase.select()
            else:
                filterStr = util.join_list(' ', self.filter)
                query = model.FileCase.raw('select * from filecase where ' + filterStr)
        except:
            Comandos.log.error('Database query error')
            print('Database query error')
            return

        # Añadir registros obtenidos a una lista
        output = [x for x in query]

        if len(output) == 0:
            print('No registers found')
        else:
            # Tabular la informacion en una tabla e imprimirla por pantalla
            table = model.get_table(output)
            print(table)

        Comandos.log.info('List finished')
