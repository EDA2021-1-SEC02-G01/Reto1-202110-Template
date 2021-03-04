"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Ordenar videos por views")
    print("0- Salir")


def initCatalog(list_type: str):
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog(list_type)


def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog)


def printResults(ord_videos, sample=10):
    size = lt.size(ord_videos)
    if size > sample:
        print("Los primeros ", sample, " videos ordenados son:")
        i = 1
        while i <= sample:
            video = lt.getElement(ord_videos, i)
            print('Titulo: ' + video['title'] + ' Canal: ' +
                  video['channel_title'] + ' Views: ' + video['views'])
            i += 1


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        list_type = input("Ingrese '1' si desea una  lista tipo 'ARRAY' o" +
                          "ingrese '2' si desea una tipo 'LINKED':\n")
        print("Cargando información de los archivos ....")
        if list_type == "1":
            catalog = initCatalog("ARRAY_LIST")
        else:
            catalog = initCatalog("SINGLE_LINKED")
        loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Paises cargados: ' + str(lt.size(catalog['countries'])))
        print('Categorias cargadas: ' + str(lt.size(catalog['categories'])))
        first_video = lt.firstElement(catalog['videos'])
        print('Titulo: ' + first_video['title'] +
              ', Canal: ' + first_video['channel_title'] +
              ', Dia de trending: ' + first_video['trending_date'] +
              ', Pais: ' + first_video['country'] +
              ', Vistas: ' + first_video['views'] +
              ', Me gusta: ' + first_video['likes'] +
              ', No me gusta: ' + first_video['dislikes']
              )
        print("\n")
        poslist = 1
        while poslist <= lt.size(catalog['categories']):
            print(lt.getElement(catalog['categories'], poslist))
            poslist += 1

    elif int(inputs[0]) == 2:
        size = input("Indique tamaño de la muestra: ")
        if int(size) <= lt.size(catalog['videos']):
            sort_type = input("Indique el tipo de ordenamiento deseado\n" +
                              "'se' para selectionsort,\n" +
                              "'ins' para insertionsort,\n" +
                              "'sa' para shellsort, \n" +
                              "'mg' para merge sort,\n" +
                              "'qk' para quick sort:\n")
            result = controller.sortVideos(catalog, int(size), sort_type)
            print("Para la muestra de", size, " elementos, el tiempo",
                  "(mseg) es: ", str(result[0]))
            printResults(result[1])
        else:
            print("No se puede ingresar un tamaño de muestra superior a los",
                  "videos cargados")
            print("Recuerde")
            print("Videos cargados:" + str(lt.size(catalog['videos'])) + "\n")
    else:
        sys.exit(0)
sys.exit(0)
