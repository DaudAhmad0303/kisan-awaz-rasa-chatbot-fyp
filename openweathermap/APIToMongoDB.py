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
def insertData(thisList):
    """This Module inserts the weather data of city fetched from `openweathermapapi` in mongodb

    Args:
        thisList (list): list of attributes i.e., `city`, `lat`, `lan`
    """
    count = 0 
    for One_loc in thisList:
        cityName = One_loc[0]
        latitude =  One_loc[1]
        langitude = One_loc[2]
        count += 1
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={langitude}&exclude=hourly,minutely,current&appid={OPEN_WEATHER_MAP_API}"
        res = requests.post(url)
        data = res.text
        parsed_json = json.loads(data)

#         create collection of city name
#         db = client[cityName]    
        collection = db[cityName]
        pprint(parsed_json)
        break
        
        for i in range(8):
            break
            day = parsed_json['daily'][i]['temp']['day']
            min = parsed_json['daily'][i]['temp']['min']
            max = parsed_json['daily'][i]['temp']['max']
            night = parsed_json['daily'][i]['temp']['night']
            eve = parsed_json['daily'][i]['temp']['eve']
            morn = parsed_json['daily'][i]['temp']['morn']
            press = parsed_json['daily'][i]['pressure']
            dew = parsed_json['daily'][i]['dew_point']
            windSpeed = parsed_json['daily'][i]['wind_speed']
            humidity = parsed_json['daily'][i]['humidity']
            cloud = parsed_json['daily'][i]['clouds']
            uvi = parsed_json['daily'][i]['uvi']
            sky =  parsed_json['daily'][i]['weather'][0]['main']
            skky =  parsed_json['daily'][i]['weather'][0]['description']

            insertData = {
                "id" : i ,
                "day temperature" : day,
                "min temperature" : min,
                "max temperature" : max,
                "night temperature" : night,
                "evening temperature": eve,
                "morning temperature": morn, 
                "pressure" : press,
                "dew point" : dew,
                "windSpeed" : windSpeed,
                "humidity" :humidity,
                "cloud":cloud,
                "uvi index":uvi, 
                "weather" : sky ,
                "sky" : skky 
                }
            
            # collection.insert_one(insertData)
            # insertData.clear()


    print("Fetch weather information of total cities {}".format(count))    


if __name__ == '__main__':

    client = pymongo.MongoClient("mongodb://localhost:27017")

    geolocations_csv_path = "D:\Daud Ahmad\FYP\Data Collection\cities geo locations.csv"
    df = pd.read_csv(filepath_or_buffer = geolocations_csv_path, encoding = "UTF-8", header = 0)
    print("File open successfully")
    print(df.head(5))
    thisList = list()
    for i in range(len(df)):
        linee = [df["city"].loc[i], df["lat"].loc[i], df["lng"].loc[i]]
        thisList.append(linee)
        break
    
    db = client["weatherData"] 
    insertData(thisList)
    print("data enter successfully in database")