# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# from openweathermap import Weather
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import pymongo as mongo
from datetime import datetime, timedelta
from pprint import pprint

client = mongo.MongoClient("mongodb://localhost:27017")
print(client)

db1 = client["KisanAwaz"]       # City Geolocations DB
db2 = client["weatherData"]     # API Fetched Weather Data DB

geoLocationsCollection = db1["CityGeoLocations"]
dumyCity = db2["لاہور"]
DBUpdateTimeStamp = dumyCity.find_one()['daily'][0]['dt']

DBUpdateTime = datetime.fromtimestamp(DBUpdateTimeStamp)

print("Database updated on:", DBUpdateTime)

allDatabases = client.list_database_names()
pprint(allDatabases)
allCollectionsInWeatherDB = list(db2.list_collections())
# pprint(allCollectionsInWeatherDB, len(len(allCollectionsInWeatherDB)))


def relative_day_no(day_name, timestamp = datetime.now().timestamp()):
    """An Intellegent Function that can return the day number
    in reference with the database update day/current day
    
    >>> 0 for today
    >>> 1 for tomorrow
    
    Similarly, day-number for current week day-name starting with today as 0

    Args:
        day_name (str): day name i.e., آج، کل، سوموار
        timestamp (class.datetime.timestamp, optional): Last update timestamp for database. Defaults to datetime.now().timestamp().

    Returns:
        int: day-number for datebase record reterival
    """
    relative_day = {
        "آج" : 0,
        "کل" : 1,
        "پرسوں" : 2
    }
    if day_name in relative_day:
        return relative_day[day_name]
    
    days_ur_en = {
        "پیر" : "Monday",
        "سوموار" : "Monday",
        "منگل" : "Tuesday",
        "بدھ" : "Wednesday",
        "جمعرات" : "Tursday",
        "جمعہ" : "Friday",
        "ہفتہ" : "Saturday",
        "اتوار" : "Sunday",
    }
    
    week_days = dict()
    
    for i in range(7):
        # Got date of current day and procedings
        date = datetime.fromtimestamp(timestamp) + timedelta(days=i)
        
        # Got today and procedings
        day = datetime.strftime(date, '%A')
        
        # print(day)
        week_days[day] = i
    
    # print(week_days)
    # pprint(days_ur_en)
    
    # {
    #     'Friday': 0,
    #     'Saturday': 1,
    #     'Sunday': 2,
    #     'Monday': 3,
    #     'Tuesday': 4,
    #     'Wednesday': 5,
    #     'Thursday': 6
    #     }
    
    if day_name in days_ur_en:
        day_en = days_ur_en[day_name]
        day_no = week_days[day_en]
        return day_no
    
    if day_name not in relative_day or day_name == None:
        return 0
    
    # # Get current TimeStamp
    # print("Current TimeStamp: ", datetime.now().timestamp())
    
    # # Get curent Time converted from current TimeStamp
    # print("curent Time converted from current TimeStamp: ", datetime.fromtimestamp(datetime.now().timestamp()))
    
    # # Get Current/ today date and time
    # print("Current/ today date and time: ", datetime.today())
    
    # # Get Current week day number
    # print("Current week day name: ", datetime.today().weekday())
    
    # # Get ToDay Name
    # print("Current week day number: ", datetime.today().strftime('%A'))
    
    # # Get Time from TimeStamp
    # print("Time from TimeStamp: ", datetime.fromtimestamp(timestamp))
    return None

"""
class ActionSetGeoLocation(Action):
    
    def name(self) -> Text:
        return "action_set_geo_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        received_city = next(tracker.get_slot("city"), None)
        document = collection1.find_one({'city': received_city})
        print(document)
        latitude = float(document['latitude'])
        longitude = float(document['longitude'])
        
        
        # dispatcher.utter_message(text="Hello World!")

        return []
"""

class ActionHelloWorld(Action):
    
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_hello_world is called")

        dispatcher.utter_message(text="Hello World!")

        return []



class ActionMornTemp(Action):
    
    def name(self) -> Text:
        return "action_utter_morn_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_morn_temp is called")
        
        # getting entity value of `city` and `day`
        received_city = next(tracker.get_latest_entity_values("city"), "لاہور")
        received_day = next(tracker.get_latest_entity_values("day"), "آج")
        
        print(received_city)
        
        most_matched_day = received_day
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day)
        print(day_no_for_DB)
        
        most_matched_city = received_city
        
        # Getting the GeoLocations' Document of `city` from Database
        document = geoLocationsCollection.find_one({'city': most_matched_city})
        print(document)
        
        latitude = float(document['latitude'])
        longitude = float(document['longitude'])
        
        # Getting Whole JSON/Document from DB of desired city
        weatherAPIDataCollection = db2[most_matched_city]
        whole_JSON = weatherAPIDataCollection.find_one(
            {
                "lat": latitude,
                "lon": longitude,
            }
        )
        # print(whole_JSON, type(whole_JSON))
        
        # Getting desired weather service
        morn_temp = whole_JSON['daily'][0]['temp']['day']
        
        morn_temp = round(float(morn_temp) - 273.15, 2)
        
        # bot_response_to_send = "{} میں زیادہ سے زیادہ درجہ حرارت 20 ڈگری سینٹی گریڈ رہے گا، جبکہ کم سے کم درجہ حرارت {} ڈگری سینٹی گریڈ رہے گا۔"
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں صبح کا درجہ حرارت {morn_temp} ڈگری سینٹی گریڈ ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں صبح کا درجہ حرارت {morn_temp} ڈگری سینٹی گریڈ رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("morn_temp", morn_temp)]
