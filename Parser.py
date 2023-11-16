import requests
import psycopg2
import datetime

def get_weather_data(api_key, city, connection):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        save_weather_data(weather_data, connection)
    else:
        print("Error: Unable to fetch weather data")

def save_weather_data(weather_data, connection):
    try:
        with connection.cursor() as cursor:
            insert_weather_query = """
                INSERT INTO WeatherData (CityName, Temperature, FeelsLikeTemperature, MinTemperature, MaxTemperature, Pressure, Humidity, Visibility, WindSpeed, WindDirection, Cloudiness, Sunrise, Sunset, DataCollectionTime, Timezone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING WeatherDataID
            """
            weather_main = weather_data['main']
            wind = weather_data['wind']
            clouds = weather_data['clouds']
            sys = weather_data['sys']

            cursor.execute(insert_weather_query, (
                weather_data['name'],
                weather_main['temp'],
                weather_main['feels_like'],
                weather_main['temp_min'],
                weather_main['temp_max'],
                weather_main['pressure'],
                weather_main['humidity'],
                weather_data.get('visibility'),
                wind['speed'],
                wind.get('deg'),
                clouds['all'],
                datetime.datetime.fromtimestamp(sys['sunrise']),
                datetime.datetime.fromtimestamp(sys['sunset']),
                datetime.datetime.fromtimestamp(weather_data['dt']),
                weather_data['timezone']
            ))
            weather_data_id = cursor.fetchone()[0]

            insert_coordinates_query = """
                INSERT INTO Coordinates (WeatherDataID, Longitude, Latitude)
                VALUES (%s, %s, %s)
            """
            coord = weather_data['coord']
            cursor.execute(insert_coordinates_query, (weather_data_id, coord['lon'], coord['lat']))

            insert_description_query = """
                INSERT INTO WeatherDescription (WeatherDataID, MainDescription, DetailedDescription, Icon)
                VALUES (%s, %s, %s, %s)
            """
            weather_desc = weather_data['weather'][0]
            cursor.execute(insert_description_query, (weather_data_id, weather_desc['main'], weather_desc['description'], weather_desc['icon']))

            connection.commit()

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()

connection = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password='12345678')

api_key = '82fb8bc18aa3f6a7f5912cb7b0d97f49'
city = 'Amsterdam'
get_weather_data(api_key, city, connection)

connection.close()

                        """Структура Таблиц
Таблица: WeatherData
WeatherDataID (int, primary key): Уникальный идентификатор записи.
CityName (varchar): Название города.
Temperature (float): Текущая температура.
FeelsLikeTemperature (float): Ощущаемая температура.
MinTemperature (float): Минимальная температура.
MaxTemperature (float): Максимальная температура.
Pressure (int): Давление в hPa.
Humidity (int): Влажность в процентах.
SeaLevel (int): Уровень моря.
GroundLevel (int): Уровень земли.
Visibility (int): Видимость в метрах.
WindSpeed (float): Скорость ветра в м/с.
WindDirection (int): Направление ветра в градусах.
Cloudiness (int): Облачность в процентах.
Sunrise (datetime): Время восхода солнца.
Sunset (datetime): Время заката солнца.
DataCollectionTime (datetime): Время сбора данных.
Timezone (int): Часовой пояс.
Таблица: Coordinates
CoordinatesID (int, primary key): Уникальный идентификатор записи.
WeatherDataID (int, foreign key): Связь с таблицей WeatherData.
Longitude (float): Долгота.
Latitude (float): Широта.
Таблица: WeatherDescription
DescriptionID (int, primary key): Уникальный идентификатор записи.
WeatherDataID (int, foreign key): Связь с таблицей WeatherData.
MainDescription (varchar): Общее описание.
DetailedDescription (varchar): Детальное описание.
Icon (varchar): Идентификатор иконки."""