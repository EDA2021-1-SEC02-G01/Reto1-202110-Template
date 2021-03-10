"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as lti
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mg
from DISClib.Algorithms.Sorting import quicksort as qk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos
listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog(list_type: str):
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'categories': None,
               'countries': None,
               'video_tags': None}

    catalog['videos'] = lt.newList(list_type)
    catalog['tags'] = lt.newList("ARRAY_LIST")
    catalog['countries'] = lt.newList("ARRAY_LIST",
                                      cmpfunction=comparecountries)
    catalog['categories'] = lt.newList("ARRAY_LIST",
                                       cmpfunction=cmpCategoriesById)

    return catalog

# Funciones para agregar informacion al catalogo


def addVideo(catalog, video):
    # Filtramos la informacion del video con lo que necesitamos
    filtrado = {'trending_date': video['trending_date'].strip(),
                'title': video['title'].strip(),
                'channel_title': video['channel_title'].strip(),
                'publish_time': video['publish_time'].strip(),
                'views': video['views'], 'likes': video['likes'].strip(),
                'dislikes': video['dislikes'].strip(),
                'country': video['country'].strip(),
                'tags': video['tags'].strip(),
                'category_id': video['category_id'].strip()}
    # Se adiciona el video a la lista de videos
    lt.addLast(catalog['videos'], filtrado)
    # Se obtienen los tags del video
    country_name = video['country'].strip()
    # Cada tag, se crea en la lista de videos del catalogo, y se
    # crea un video en la lista de dicho tag (apuntador al libro)
    addVideoCountry(catalog, country_name, video)


def addVideoCountry(catalog, country_name, video):
    """
    Adiciona un tag a lista de tags, la cual guarda referencias
    a los videos que tienen ese tag
    """
    countries = catalog['countries']
    posCountry = lt.isPresent(countries, country_name)
    if posCountry > 0:
        country = lt.getElement(countries, posCountry)
    else:
        country = newCountry(country_name)
        lt.addLast(countries, country)
    lt.addLast(country['videos'], video)


def addCategory(catalog, category):
    """
    Adiciona una categoría a la lista de categorías
    """
    c = newCategory(category['id'], category['name'], catalog['videos'])
    if c not in catalog['categories']['elements']:
        lt.addLast(catalog['categories'], c)


# Funciones para creacion de datos

def newCountry(name):
    """
    Crea una nueva estructura para modelar los libros de
    un autor y su promedio de ratings
    """
    country = {'name': "", "videos": None}
    country['name'] = name.strip()
    country['videos'] = lt.newList('ARRAY_LIST')
    return country


def newCategory(id, name, videos):
    """
    Esta estructura crea las categorías utilizadas para marcar videos.
    """
    category = {'category-id': '', 'name': '', 'videos': ''}
    category['name'] = name.strip()
    category['category-id'] = id
    videosByCategory = categorySort(id, videos)
    category['videos'] = videosByCategory
    return category


# Funciones de consulta
def videosCountryCategory(category_name, country, n_videos):
    pass


# Funciones utilizadas para comparar elementos dentro de una lista
def comparecountries(countryname1, country):
    if (countryname1.lower() in country['name'].lower()):
        return 0
    return -1


def cmpVideosByViews(video1, video2):
    """
    Devuelve verdadero (True) si los 'views' de video1
    son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'views'
    video2: informacion del segundo video que incluye su valor 'views'
    """
    return int(video1['views']) > int(video2['views'])


def cmpCategoriesById(category1, category2):
    return int(category1["category-id"]) < int(category1["category-id"])


# Funciones de ordenamiento

def sortVideos(catalog, size, sort_type):
    sub_list = lt.subList(catalog['videos'], 1, size)
    sub_list = sub_list.copy()
    start_time = time.process_time()
    if sort_type == "se":
        sorted_list = se.sort(sub_list, cmpVideosByViews)
    elif sort_type == "ins":
        sorted_list = ins.sort(sub_list, cmpVideosByViews)
    elif sort_type == "sa":
        sorted_list = sa.sort(sub_list, cmpVideosByViews)
    elif sort_type == "mg":
        sorted_list = mg.sort(sub_list, cmpVideosByViews)
    elif sort_type == "qk":
        sorted_list = qk.sort(sub_list, cmpVideosByViews)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list


def categorySort(category_id, videos):
    iterator = lti.newIterator(videos)
    sub_list = lt.newList('ARRAY_LIST')
    while lti.hasNext(iterator):
        video = lti.next(iterator)
        if int(video['category_id']) == int(category_id):
            lt.addLast(sub_list, video)
    return sub_list


def sortCountry(catalog, category_name, country_name):
    iteratorCategoriesAll = lti.newIterator(catalog['categories'])
    category = None
    while lti.hasNext(iteratorCategoriesAll):
        element = lti.next(iteratorCategoriesAll)
        print(category_name + element['name'])
        if category_name.lower() == element['name'].lower():
            category = element
            break

    iteratorCountry = lti.newIterator(category['videos'])
    country_list = lt.newList('ARRAY_LIST')
    while lti.hasNext(iteratorCountry):
        video = lti.next(iteratorCountry)
        if country_name.lower() == video['country'].lower():
            lt.addLast(country_list, video)
    return country_list


def sortVideoslt(videos):
    sorted_list = mg.sort(videos, cmpVideosByViews)
    return sorted_list
