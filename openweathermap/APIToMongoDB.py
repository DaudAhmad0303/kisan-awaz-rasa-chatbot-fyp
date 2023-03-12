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
    """This Module inserts the weather data of cities, fetched from `openweathermapapi` in mongodb

    Args:
        cities_geolocation_df (DataFrame.Pandas): Pandas DataFrame containing following fields:
        i.e., `city`, `lat`, `lng`
    """
    
    # create collection for WeatherForecast
    weather_forecast_collection = kisan_awaz_db["WeatherForecast"]
    
    # Fetching documents from weather_forecast_collection, if there inserted previously and 
    # storing all the cities name in a single list
    previous_docs = weather_forecast_collection.find({}, {"_id": 1})
    previous_docs_lst = list(map(lambda dict1: dict1["_id"], previous_docs))
    
    count = 0
    for i in cities_geolocation_df.index:
        cityName = cities_geolocation_df.loc[i]['city']
        latitude =  cities_geolocation_df.loc[i]['lat']
        langitude = cities_geolocation_df.loc[i]['lng']
        if cityName not in previous_docs_lst:
            url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={langitude}&exclude=hourly,minutely,current&appid={OPEN_WEATHER_MAP_API}&units=metric"
            res = requests.post(url)
            data = res.text
            parsed_json = json.loads(data)
            
            parsed_json["_id"] = cityName
            weather_forecast_collection.insert_one(parsed_json)
            count += 1
        break

    print("Fetched and Inserted weather information of total cities {}".format(count))

def updateData(cities_geolocation_df):
    """This Module updates the weather data of cities, fetched from `openweathermapapi` in mongodb

    Args:
        cities_geolocation_df (DataFrame.Pandas): Pandas DataFrame containing following fields:
        i.e., `city`, `lat`, `lng`
    """
    
    # create collection for WeatherForecast
    weather_forecast_collection = kisan_awaz_db["WeatherForecast"]
    
    count = 0 
    for i in cities_geolocation_df.index:
        cityName = cities_geolocation_df.loc[i]['city']
        latitude =  cities_geolocation_df.loc[i]['lat']
        langitude = cities_geolocation_df.loc[i]['lng']
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={langitude}&exclude=hourly,minutely,current&appid={OPEN_WEATHER_MAP_API}&units=metric"
        res = requests.post(url)
        data = res.text
        parsed_json = json.loads(data)
        
        parsed_json["_id"] = cityName
        updated_doc = weather_forecast_collection.find_one_and_replace({"_id": cityName}, parsed_json)
        count += 1
        break
    print("Fetched and Updated weather information of total cities {}".format(count))
    

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
    # insertData(cities_geolocation_df)
    # updateData(cities_geolocation_df)
    print("Data enter successfully in database...!")