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
    filtrado = {'video_id': video['video_id'].strip(),
                'trending_date': video['trending_date'].strip(),
                'title': video['title'].strip(),
                'channel_title': video['channel_title'].strip(),
                'publish_time': video['publish_time'].strip(),
                'views': video['views'],
                'likes': video['likes'].strip(),
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
    addVideoCountry(catalog, country_name, filtrado)


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
    country = {'name': "", 'videos': ""}
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


def getTrendVidByCountry(catalog, country_name):
    countries = catalog['countries']
    posCountry = lt.isPresent(countries, country_name)
    if posCountry > 0:
        country = lt.getElement(countries, posCountry)
    mg.sort(country['videos'], cmpVideosByTitle)
    iteratorVid = lti.newIterator(country['videos'])
    trendVids = lt.newList("ARRAY_LIST", cmpfunction=compareVideoName)
    while lti.hasNext(iteratorVid):
        video = lti.next(iteratorVid)
        vidName = video['title']
        posVid = lt.isPresent(trendVids, vidName)
        if posVid > 0:
            el = lt.getElement(trendVids, posVid)
            el['cuenta'] += 1
        else:
            lt.addLast(trendVids, {"info": video, "cuenta": 1})
    sortedTrendVids = mg.sort(trendVids, cmpVideosByDays)
    firstTrendVid = lt.firstElement(sortedTrendVids)
    return firstTrendVid


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


def cmpVideosByDays(video1, video2):
    """
    Devuelve True si los dias que estuvo en trend el video 1 son mayores
    que los del video2
    """
    return video1['cuenta'] > video2['cuenta']


def cmpVideosByTitle(video1, video2):
    return video1['title'] < video2['title']


def compareVideoName(videoname1, video):
    if (videoname1.lower() in video['info']['title'].lower()):
        return 0
    return -1


def cmpLikes(video1, video2):
    return int(video1['likes']) < int(video2['likes'])


def cmpTitleAlphabet(video1, video2):
    return str(video1['title']) < str(video2['title'])


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


def sortTagsName(catalog, tag_name):
    iteratorTags = lti.newIterator(catalog['videos'])
    tag_list = lt.newList('ARRAY_LIST')
    while lti.hasNext(iteratorTags):
        video = lti.next(iteratorTags)
        lista = video['tags'].lower()
        if tag_name.lower() in lista:
            lt.addLast(tag_list, video)
    return tag_list


def sortLikesTags(catalog, tag_name, n_videos):
    sortTags = sortTagsName(catalog, tag_name)
    merge = mg.sort(sortTags, cmpLikes)
    return lt.subList(merge, 0, n_videos)


def sortTitles(catalog):
    # list_videos = lt.sublist(catalog,1,lt.size(catalog))
    videos = catalog['videos']
    sortAlphabeticly = mg.sort(videos, cmpTitleAlphabet)
    return sortAlphabeticly


def sortTrendigDates(catalog, category_name):
    iteratorCategoriesAll = lti.newIterator(catalog['categories'])
    category = None
    while lti.hasNext(iteratorCategoriesAll) and category == None:
        element = lti.next(iteratorCategoriesAll)
        print(category_name + element['name'])
        if category_name.lower() == element['name'].lower():
            category = element

    sortTitleAlphabeticly = sortTitles(category)
    iteratorTrending = lti.newIterator(sortTitleAlphabeticly)
    lista = lt.newList('ARRAY_LIST', cmpfunction=compareVideoName)
    while lti.hasNext(iteratorTrending):
        element = lti.next(iteratorTrending)
        vidName = element['title']
        posVid = lt.isPresent(lista, vidName)
        if posVid > 0:
            el = lt.getElement(lista, posVid)
            el['cuenta'] += 1
        else:
            lt.addLast(lista, {'info': element, 'cuenta': 1})
    lista_ordenada = mg.sort(lista, cmpVideosByDays)
    return lista_ordenada
