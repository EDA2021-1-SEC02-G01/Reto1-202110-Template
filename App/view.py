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
    print("2- n videos con mas views que son tendencia en un pais " +
          "determinada una categoria especifica (Req.1)")
    print("3- conocer cuál es el video que más días ha sido trending para un" +
          " país específico. (Req. 2) ")
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
        list_type = input("Ingrese '1' si desea una  lista tipo 'ARRAY' o " +
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
        print(first_video)
        poslist = 1

    elif int(inputs[0]) == 2:
        category_name = input("Indique el nombre de la categoria que quiere " +
                              "consultar: ")
        country = input("Indique el pais de los videos que quiere consultar: ")
        n_videos = int(input("Indique el tamaño de la muestra que quiere " +
                             "consultar: "))
        videosByCC = controller.sortCountry(catalog, category_name, country)
        videosCCSorted = controller.sortVideolt(videosByCC)
        counter = 1
        while counter <= n_videos:
            video = lt.getElement(videosCCSorted, counter)
            print('trending_date: ' + video['trending_date'],
                  'title: ' + video['title'],
                  'channel_title: ' + video['channel_title'],
                  'publish_time: ' + video['publish_time'],
                  'views: ' + video['views'],
                  'likes: ' + video['likes'],
                  'dislikes: ' + video['dislikes'])
            counter += 1

    elif int(inputs[0]) == 3:
        country_name = input("Indique el nombre del país que desea buscar: ")
        trendVid = controller.getTrendVidByCountry(catalog, country_name)
        trendInfo = trendVid['info']
        cuenta = trendVid['cuenta']
        print("Title: " + trendInfo['title'])
        print("Channel Title" + trendInfo['channel_title'])
        print("Country: " + trendInfo['country'])
        print("Numero de dias en tendencia: " + str(cuenta))

    else:
        sys.exit(0)
sys.exit(0)
