import pandas as pd
import requests
from dotenv import load_dotenv
from pathlib import Path
from os import getenv
from pprint import pprint
import json
import pymongo
import colorama
from datetime import datetime
import os

# dotenv_path = Path("..\\.env")
# load_dotenv(dotenv_path=dotenv_path)
# OPEN_WEATHER_MAP_API = getenv("OPEN_WEATHER_MAP_API")

# Database Client Created
# client = pymongo.MongoClient("mongodb://localhost:27017")
try:
    REMOTE_DB_URL = os.environ["REMOTE_DB_URL"]
    OPEN_WEATHER_MAP_API = os.environ["OPEN_WEATHER_MAP_API"]
except KeyError:
    REMOTE_DB_URL = "Token not available!"
    OPEN_WEATHER_MAP_API = "Token not available!"
    logger.info("Token not available!")

# REMOTE_DB_URL = getenv("REMOTE_DB_URL")
client = pymongo.MongoClient(REMOTE_DB_URL)

kisan_awaz_db = client["KisanAwaz"]

def progress_bar(progress, total, color=colorama.Fore.YELLOW):
    """Shows the progress bar based on the parameters `progress` and `total`

    Args:
        progress (int): The amount of task that has been done
        total (_type_): The total amount of task that has to be.
        color (colorama.Fore.[ANY_COLOR], optional): The color of the bar which you wants to show for progress bar. Defaults to colorama.Fore.YELLOW.
    """
    percent = 100 * (progress / float(total))
    bar = "█" * int(percent) + '-' * (100 - int(percent))
    print(color + f"\r|{bar}| {percent:.2f}%", end="\r")
    
    if progress == total:
        print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%", end="\r")

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
    # previous_docs_lst = list()
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
            progress_bar(count+1, len(cities_geolocation_df) - len(previous_docs_lst))
            count += 1
        break
    print(colorama.Fore.RESET)
    print("\nFetched and Inserted weather information of total cities {}\n".format(count))

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
        # print(updated_doc)
        progress_bar(count+1, len(cities_geolocation_df))
        count += 1
        # break
    print(colorama.Fore.RESET)
    print("\nFetched and Updated weather information of total cities {}\n".format(count))

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
    print("City Geolocation data loaded form DB successfully...\n")
    
    # print(cities_geo_locations_df.loc[0:4])
    return cities_geo_locations_df

def load_cities_from_csv():
    """Loads `CSV` from local Disk, store in DataFrame and returns it.

    Returns:
        Pandas.DataFrame: DataFrame Containing Cities Geolocations
    """
    cities_geo_locations_df = pd.read_csv(
        filepath_or_buffer = Path("cities geo locations for 490.csv"),
        encoding = "UTF-8",
        header = 0
    )
    print("CSV file open successfully...\n")
    
    return cities_geo_locations_df

def time_DB_updated(formated = True):
    """This function returns the time when the database was last updated.

    Args:
        formated (bool, optional): whether needs formated string of time or `datetime.timestamp`. Defaults to True.

    Returns:
        timestamp: DB last updated time [formated]
    """
    weather_forecast_collection = kisan_awaz_db["WeatherForecast"]
    for doc in weather_forecast_collection.find({"_id":"کراچی"}, {"daily": 1}):
        if not formated:
            return doc['daily'][0]['dt']
        else:
            return "Date & Time: " + str(datetime.fromtimestamp(doc['daily'][0]['dt']))
    
if __name__ == '__main__':
    
    # cities_geolocation_df = load_cities_from_csv()
    cities_geolocation_df = load_cities_from_db()

    print("Last Updated", time_DB_updated())
    
    # Un-comment any of the following line to insert or update data in database
    # insertData(cities_geolocation_df)
    updateData(cities_geolocation_df)
    
    print("New", time_DB_updated())
    print("Data enter successfully in database...!")
