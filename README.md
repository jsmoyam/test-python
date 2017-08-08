# test-python

Fichero principal Comandos.py<br />
  python3 Comandos.py<br />
  
Es necesario tener las librerias peewee y terminaltables instaladas:<br />
  pip3 install peewee<br />
  pip3 install terminaltables<br />
  
Una vez dentro hay que definir las variables INCOMING_FOLDER y DESTINATION_FOLDER:<br />
  set INCOMING_FOLDER /path/to/incoming/folder<br />
  set DESTINATION_FOLDER /path/to/destination/folder<br />

O bien crear un script con esos dos comandos ya incluidos y ejecutarlo con <br />
  run script.one<br />
  
Para ver todos los comandos disponibles escribir "help". Haciendo "help comando" se puede visualizar el detalle de cada comando.

El script change_permissions.sh contiene el script bash para visualizar ficheros/directorios en funcion de permisos y modificar permisos de manera masiva:<br />
  change_permissions.sh /folder1 /folder2 /folder3 ... /folderN<br />
