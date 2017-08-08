# test-python

Fichero principal Comandos.py: 
  python3 Comandos.py
  
Es necesario tener las librerias peewee y terminaltables instaladas:
  pip3 install peewee
  pip3 install terminaltables
  
Una vez dentro hay que definir las variables INCOMING_FOLDER y DESTINATION_FOLDER:
  set INCOMING_FOLDER /path/to/incoming/folder
  set DESTINATION_FOLDER /path/to/destination/folder

O bien crear un script con esos dos comandos ya incluidos y ejecutarlo con 
  run script.one

El script change_permissions.sh contiene el script bash para visualizar ficheros/directorios en funcion de permisos y modificar permisos de manera masiva
