import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
from utils import get_spn, distance_between_points

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

response = requests.get(
    "https://search-maps.yandex.ru/v1/?apikey=5cd985b0-e0e1-4c0e-acae-da6b86a27926&text=аптека&ll="
    f"{toponym_coodrinates.replace(' ', ',')}&results=500&spn={','.join([*get_spn(toponym)])}&"
    f"type=biz&lang=ru&format=json"
)
data = response.json()["features"]
objects = [(distance_between_points((float(toponym_longitude), float(toponym_lattitude)),
                                    e["geometry"]["coordinates"]),
            e["properties"]) for e in data]
for e in sorted(objects, key=lambda e: e[0]):
    print(e)

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([*get_spn(data)]),
    "l": "map",
    "pt": toponym_coodrinates.replace(" ", ",") + ",pm2rdm"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
