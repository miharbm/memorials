import pandas as pd
import folium
import json
import branca
import math

from matplotlib import pyplot as plt


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

# Координаты нулевого километра Москвы
moscow_center = (55.7539303, 37.620795)


def calculate_distance(lat2, lon2):
    lat1, lon1 = moscow_center
    # # lat2, lon2 = coord
    #
    # # Радиус Земли в километрах
    radius = 6371.0
    #
    # # Перевод координат в радианы
    # # lat1 = math.radians(lat1)
    # # lon1 = math.radians(lon1)
    # # lat2 = math.radians(lat2)
    # # lon2 = math.radians(lon2)
    #
    # # Разница между долготами и широтами
    # dlon = lon2 - lon1
    # dlat = lat2 - lat1
    #
    # # Формула гаверсинусов
    # a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    # c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    #
    # # Расстояние между точками
    # distance = radius * c

    distance = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)

    return distance * radius


distances = []
for i in range(len(data['longitude'])):
    # x = calculate_distance(data['latitude'].mean(), data['longitude'].mean())
    x = calculate_distance(data['longitude'][i], data['latitude'][i])
    distances.append(x)
print(distances)
# Пример использования функции
# distance_from_center = calculate_distance((55.762309204, 37.626996138))
# print("Расстояние от нулевого километра Москвы:", distance_from_center, "км")


# Создание графика зависимости расстояния от года
plt.figure(figsize=(10, 6))
plt.plot(data['year'], distances, marker='o')
plt.title('Зависимость расстояния от года')
plt.xlabel('Год')
plt.ylabel('Расстояние от нулевого километра, км')
plt.grid(True)
plt.show()
