import pandas as pd
import requests
from dotenv import load_dotenv
from pathlib import Path
from os import getenv
from pprint import pprint
import json
import pymongo

dotenv_path = Path("D:\Daud Ahmad\FYP\RASA Implementation\code\.env")
load_dotenv(dotenv_path=dotenv_path)
OPEN_WEATHER_MAP_API = getenv("OPEN_WEATHER_MAP_API")

# Database Client Created
client = pymongo.MongoClient("mongodb://localhost:27017")
kisan_awaz_db = client["KisanAwaz"]

def insertData(cities_geolocation_df):
    """This Module inserts the weather data of city fetched from `openweathermapapi` in mongodb

    Args:
        cities_geolocation_df (DataFrame.Pandas): Pandas DataFrame containing following fields:
        i.e., `city`, `lat`, `lng`
    """
    
    # create collection for WeatherForecast
    weather_forecast_collection = kisan_awaz_db["WeatherForecast"]
    
    previous_docs = weather_forecast_collection.find({}, {"_id": 1})
    previous_docs_lst = list(map(lambda dict1: dict1["_id"], previous_docs))
    count = 0
    for i in cities_geolocation_df.index:
        cityName = cities_geolocation_df.loc[i]['city']
        latitude =  cities_geolocation_df.loc[i]['lat']
        langitude = cities_geolocation_df.loc[i]['lng']
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={langitude}&exclude=hourly,minutely,current&appid={OPEN_WEATHER_MAP_API}&units=metric"
        res = requests.post(url)
        data = res.text
        parsed_json = json.loads(data)
        pprint(parsed_json)
        
        parsed_json["_id"] = cityName
        if cityName not in previous_docs_lst:
            weather_forecast_collection.insert_one(parsed_json)
            count += 1
        break

        # for i in range(8):
        #     break
        #     day = parsed_json['daily'][i]['temp']['day']
        #     min = parsed_json['daily'][i]['temp']['min']
        #     max = parsed_json['daily'][i]['temp']['max']
        #     night = parsed_json['daily'][i]['temp']['night']
        #     eve = parsed_json['daily'][i]['temp']['eve']
        #     morn = parsed_json['daily'][i]['temp']['morn']
        #     press = parsed_json['daily'][i]['pressure']
        #     dew = parsed_json['daily'][i]['dew_point']
        #     windSpeed = parsed_json['daily'][i]['wind_speed']
        #     humidity = parsed_json['daily'][i]['humidity']
        #     cloud = parsed_json['daily'][i]['clouds']
        #     uvi = parsed_json['daily'][i]['uvi']
        #     sky =  parsed_json['daily'][i]['weather'][0]['main']
        #     skky =  parsed_json['daily'][i]['weather'][0]['description']

        #     insertData = {
        #         "id" : i ,
        #         "day temperature" : day,
        #         "min temperature" : min,
        #         "max temperature" : max,
        #         "night temperature" : night,
        #         "evening temperature": eve,
        #         "morning temperature": morn, 
        #         "pressure" : press,
        #         "dew point" : dew,
        #         "windSpeed" : windSpeed,
        #         "humidity" :humidity,
        #         "cloud":cloud,
        #         "uvi index":uvi, 
        #         "weather" : sky ,
        #         "sky" : skky 
        #         }
            
        # collection.insert_one(insertData)
        # insertData.clear()

    print("Fetched and Inserted weather information of total cities {}".format(count))

def UpdateData(cities_geolocation_df):
    """This Module inserts the weather data of city fetched from `openweathermapapi` in mongodb

    Args:
        cities_geolocation_df (DataFrame.Pandas): Pandas DataFrame containing following fields:
        i.e., `city`, `lat`, `lng`
    """
    count = 0 
    for i in cities_geolocation_df.index:
        cityName = cities_geolocation_df.loc[i]['city']
        latitude =  cities_geolocation_df.loc[i]['lat']
        langitude = cities_geolocation_df.loc[i]['lng']
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={langitude}&exclude=hourly,minutely,current&appid={OPEN_WEATHER_MAP_API}&units=metric"
        res = requests.post(url)
        data = res.text
        parsed_json = json.loads(data)
        pprint(parsed_json)
        count += 1
        
#       create collection for WeatherForecast
        weather_forecast_collection = kisan_awaz_db["WeatherForecast"]
        
        parsed_json["_id"] = cityName
        weather_forecast_collection.insert_one(parsed_json)
        break

def load_cities_from_db():
    """Loads Collection from Database and saves documents from
    collection in a single Pandas Dataframe and returns it.

    Returns:
        Pandas.DataFrame: DataFrame Containing Cities Geolocations
    """
    
    geolocation_collection = kisan_awaz_db["CityGeoLocations"]
    
    cities_geo_locations_df = pd.DataFrame(columns=['city', 'lat', 'lng'])
    for doc in geolocation_collection.find({}):
        cities_geo_locations_df.loc[len(cities_geo_locations_df)] = [
            doc['city'],
            doc['latitude'],
            doc['longitude']
        ]
    print("File open successfully")
    
    # print(cities_geo_locations_df.loc[0:4])
    return cities_geo_locations_df

def load_cities_from_csv():
    """Loads `CSV` from local Disk, store in DataFrame and returns it.

    Returns:
        Pandas.DataFrame: DataFrame Containing Cities Geolocations
    """
    cities_geo_locations_df = pd.read_csv(
        filepath_or_buffer = Path("D:\Daud Ahmad\FYP\Data Collection\cities geo locations.csv"),
        encoding = "UTF-8",
        header = 0
    )
    print("File open successfully")
    # print(cities_geo_locations_df.head(5))
    # thisList = list()
    # for i in range(len(cities_geolocations_df)):
    #     linee = [
    #         df["city"].loc[i],
    #         df["lat"].loc[i],
    #         df["lng"].loc[i]
    #     ]
    #     thisList.append(linee)
    #     break
    
    return cities_geo_locations_df


if __name__ == '__main__':

    client = pymongo.MongoClient("mongodb://localhost:27017")
    
    # cities_geolocation_df = load_cities_from_csv()
    cities_geolocation_df = load_cities_from_db()
    
    # db = client["weatherData"]
    insertData(cities_geolocation_df)
    # print("data enter successfully in database")