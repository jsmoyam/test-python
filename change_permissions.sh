#!/bin/bash

join_arguments() {
    for p in $@
    do
        bar="$bar^$p$|"
    done
    regexp=${bar::-1}
}

printf "Directorios para los que el usuario tiene permisos de lectura y ejecucion\n"
find $@ -readable -and -executable -type d -maxdepth 0
printf "\n"

printf "Ficheros o directorios para los que se tiene permiso de ejecucion y lectura, dentro de los dados inicialmente\n"
# La salida del comando find muestra tambien los directorios iniciales que se pasan como argumento del script
# Con esto se eliminan dichos directorios de la salida del comando
# Solucion: unir todos los argumentos (directorios) para formar la expresion regular perl "*directorio1$|^directorio2$|...|^directorioN$"
# La funcion deja la union en la variable regexp
# Para eliminar dicho comportamiento solo hay que quitar el grep inverso
join_arguments $@

# Con 2>/dev/null se eliminan salidas de find debidas a no poder acceder a archivos/directorios por faltar permiso de lectura
find $@ -readable -and -executable 2>/dev/null | grep -v --perl-regex $regexp
printf "\n"

printf "Otorgar permisos de lectura y ejecucion a todos los ficheros dentro de los directorios accesibles pasados como argumento\n"
find $@ -exec chmod -R u+r+x {} \;