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

import time
import tracemalloc
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
    print("2- Req. 1: n videos con mas views que son tendencia en un pais " +
          "determinada una categoria especifica.")
    print("3- Req. 2: Video que mas tiempo ha estado trendig en un pais.")
    print("4- Req. 3: Video que mas dias ha sido trending en una " +
          "categoria especifica.")
    print("5- Req. 4: n videos diferentes con mas likes con un tag " +
          "especifico.")
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
    categories = controller.loadData(catalog)
    return categories


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
        answer = loadData(catalog)
        print(answer)
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
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
        print("\n")
        poslist = 1

    elif int(inputs[0]) == 2:
        # toma de tiempo y memoria
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()
        # toma de tiempo y memoria
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
        # toma de tiempo y memoria
        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        # toma de tiempo y memoria
        print("Tiempo [ms]: " + str(round(delta_time, 3)), "  ||  ",
              "Memoria [kB]: ", str(round(delta_memory, 3)))
        print("\n")

    elif int(inputs[0]) == 3:
        # toma de tiempo y memoria
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()
        # toma de tiempo y memoria
        country_name = input("Indique el nombre del país que desea buscar: ")
        trendVid = controller.getTrendVidByCountry(catalog, country_name)
        trendInfo = trendVid['info']
        cuenta = trendVid['cuenta']
        print("Title: " + trendInfo['title'])
        print("Channel Title" + trendInfo['channel_title'])
        print("Country: " + trendInfo['country'])
        print("Numero de dias en tendencia: " + str(cuenta))
        # toma de tiempo y memoria
        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        # toma de tiempo y memoria
        print("Tiempo [ms]: " + str(round(delta_time, 3)), "  ||  ",
              "Memoria [kB]: ", str(round(delta_memory, 3)))
        print("\n")

    elif int(inputs[0]) == 4:
        # toma de tiempo y memoria
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()
        # toma de tiempo y memoria
        category_name = input("Ingrese el nombre de la categoria que quiere " +
                              "buscar: ")
        cat_vid = controller.sortTrending(catalog, category_name)
        elemento = lt.firstElement(cat_vid)
        print(elemento)
        print('title: ' + elemento['info']['title'])
        print('channel_title: ' + elemento['info']['channel_title'])
        print('category_id: ' + elemento['info']['category_id'])
        print('numero de dias: ' + str(elemento['cuenta']))
        # toma de tiempo y memoria
        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        # toma de tiempo y memoria
        print("Tiempo [ms]: " + str(round(delta_time, 3)), "  ||  ",
              "Memoria [kB]: ", str(round(delta_memory, 3)))
        print("\n")

    elif int(inputs[0]) == 5:
        # toma de tiempo y memoria
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()
        # toma de tiempo y memoria
        tag_name = input("Ingrese el nombre del tag que quiere buscar: ")
        n_videos = int(input("Ingrese el numero de la muestra: "))
        sortLikesTags = controller.sortLikesTags(catalog, tag_name, n_videos)
        counter = 1
        while counter <= n_videos:
            video = lt.getElement(sortLikesTags, counter)
            print('\n' +
                  'title: ' + video['title'],
                  'channel_title: ' + video['channel_title'],
                  'publish_time: ' + video['publish_time'],
                  'views: ' + video['views'],
                  'likes: ' + video['likes'],
                  'dislikes: ' + video['dislikes'],
                  'tags: ' + video['tags'] + '/n'
                  )
            counter += 1
        # toma de tiempo y memoria
        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        # toma de tiempo y memoria
        print("Tiempo [ms]: " + str(round(delta_time, 3)), "  ||  ",
              "Memoria [kB]: ", str(round(delta_memory, 3)))
        print("\n")

    else:
        sys.exit(0)
sys.exit(0)
