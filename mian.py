import pandas as pd
import folium
import json
import branca


# Функция для загрузки и предварительной обработки данных из JSON
def load_and_preprocess_data(file_path):
    with open(file_path, 'r', encoding='windows-1251', newline='') as file:
        json_data = json.load(file)

    data = {'latitude': [], 'longitude': [], 'year': []}

    for entry in json_data:
        coordinates = entry.get('geoData', {}).get('coordinates', [])
        installation_date = entry.get('InstallationDate')

        if len(coordinates) == 2 and installation_date:
            try:
                year = int(installation_date.split('.')[-1])
            except ValueError:
                print(f"Skipping entry with invalid year: {entry}")
                continue

            lat, lon = coordinates
            if year > 1700:
                data['latitude'].append(lat)
                data['longitude'].append(lon)
                data['year'].append(year)
        else:
            print(f"Skipping malformed entry: {entry}")

    return pd.DataFrame(data)


# Загрузка и обработка данных из JSON
data = load_and_preprocess_data('./data.json')

# Создаем базовую карту
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=5)

# Генерируем цвета для разных годов с помощью branca.colormap
years = data['year'].unique()
colormap = branca.colormap.linear.YlOrRd_09.scale(years.min(), years.max())

# Добавляем цветовую легенду на карту
colormap.caption = 'Installation Year'
colormap.add_to(m)

# Добавляем точки на карту с цветами по годам
for index, row in data.iterrows():
    folium.CircleMarker(
        # location=(row['latitude'], row['longitude']),
        location=(row['longitude'], row['latitude']),
        radius=5,
        color=colormap(row['year']),
        fill=True,
        fill_color=colormap(row['year']),
        fill_opacity=0.6
    ).add_to(m)

# Сохраняем карту в HTML файл
m.save('map.html')

# import pandas as pd
# import folium
# import json
# import branca
#
#
# # Функция для загрузки и предварительной обработки данных из JSON
# def load_and_preprocess_data(file_path):
#     # with open(file_path, 'r', encoding='utf-8') as file:
#     #     json_data = json.load(file)
#     json_data = json.load(file_path)
#         # print(json_data)
#
#     data = {'latitude': [], 'longitude': [], 'year': []}
#
#     for entry in json_data:
#         coordinates = entry.get('geoData', {}).get('coordinates', [])
#         installation_date = entry.get('InstallationDate')
#
#         if len(coordinates) == 2 and installation_date:
#             try:
#                 year = int(installation_date.split('.')[-1])
#             except ValueError:
#                 print(f"Skipping entry with invalid year: {entry}")
#                 continue
#
#             lat, lon = coordinates
#             data['latitude'].append(lat)
#             data['longitude'].append(lon)
#             data['year'].append(year)
#         else:
#             print(f"Skipping malformed entry: {entry}")
#
#     return pd.DataFrame(data)
#
#
# # Загрузка и обработка данных из JSON
# data = load_and_preprocess_data('data.json')
#
# print(data)
#
# # Создаем базовую карту
# m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=5)
#
# # Генерируем цвета для разных годов с помощью branca.colormap
# years = data['year'].unique()
# colormap = branca.colormap.linear.YlOrRd_09.scale(years.min(), years.max())
#
# # Добавляем цветовую легенду на карту
# colormap.caption = 'Installation Year'
# colormap.add_to(m)
#
# # Добавляем точки на карту с цветами по годам
# for index, row in data.iterrows():
#     folium.CircleMarker(
#         location=(row['latitude'], row['longitude']),
#         radius=5,
#         color=colormap(row['year']),
#         fill=True,
#         fill_color=colormap(row['year']),
#         fill_opacity=0.6
#     ).add_to(m)
#
# # Сохраняем карту в HTML файл
# m.save('map.html')

# import pandas as pd
# import folium
# import json
# import branca
#
# # Пример JSON данных
# json_data = [
#     {
#         "global_id": 2812434,
#         "ID": 1645,
#         "Name": "Мемориальная доска памяти ополченцев Народного комиссариата иностранных дел РФ",
#         "Text": "Победа будет за нами...",
#         "AdmArea": "Центральный административный округ",
#         "District": "Мещанский район",
#         "Location": "город Москва, улица Кузнецкий Мост, дом 21/5, строение 1",
#         "InstallationDate": "10.02.2014",
#         "Form": "сложной формы",
#         "Details": "С барельефным изображением ополченцев на фоне города",
#         "Material": "бронза",
#         "InventoryDate": "01.03.2023",
#         "Condition": "полная",
#         "CommonInfo": "Размеры: 150 х 240 см.",
#         "UNOM": "2125855",
#         "geoData": {"coordinates": [37.626996138, 55.762309204], "type": "Point"},
#         "geodata_center": {"coordinates": [37.626996138, 55.762309204], "type": "Point"}
#     }
#     # добавьте другие записи здесь
# ]
#
#
# # Функция для загрузки и предварительной обработки данных из JSON
# def load_and_preprocess_data(json_data):
#     data = {'latitude': [], 'longitude': [], 'year': []}
#
#     for entry in json_data:
#         coordinates = entry.get('geoData', {}).get('coordinates', [])
#         installation_date = entry.get('InstallationDate')
#
#         if len(coordinates) == 2 and installation_date:
#             try:
#                 year = int(installation_date.split('.')[-1])
#             except ValueError:
#                 print(f"Skipping entry with invalid year: {entry}")
#                 continue
#
#             lat, lon = coordinates
#             data['latitude'].append(lat)
#             data['longitude'].append(lon)
#             data['year'].append(year)
#         else:
#             print(f"Skipping malformed entry: {entry}")
#
#     return pd.DataFrame(data)
#
#
# # Загрузка и обработка данных из JSON
# data = load_and_preprocess_data("data.json")
#
#
# # Создаем базовую карту
# m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=5)
#
# # Генерируем цвета для разных годов с помощью branca.colormap
# years = data['year'].unique()
# colormap = branca.colormap.linear.YlOrRd_09.scale(years.min(), years.max())
#
# # Добавляем цветовую легенду на карту
# colormap.caption = 'Installation Year'
# colormap.add_to(m)
#
# # Добавляем точки на карту с цветами по годам
# for index, row in data.iterrows():
#     folium.CircleMarker(
#         location=(row['longitude'], row['latitude']),  # обратите внимание на порядок координат
#         radius=5,
#         color=colormap(row['year']),
#         fill=True,
#         fill_color=colormap(row['year']),
#         fill_opacity=0.6
#     ).add_to(m)
#
# # Сохраняем карту в HTML файл
# m.save('map.html')
