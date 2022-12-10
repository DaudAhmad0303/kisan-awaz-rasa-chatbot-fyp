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
from .fuzzyString import get_matched_name
from .relativeDayNo import relative_day_no

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
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day)
        print(day_no_for_DB)
        
        # Getting most matched city name with custom function
        most_matched_city = get_matched_name(received_city, "city")[0]
        
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
        morn_temp = whole_JSON['daily'][0]['temp']['morn']
        
        morn_temp = round(float(morn_temp) - 273.15, 2)
        
        # bot_response_to_send = "{} میں زیادہ سے زیادہ درجہ حرارت 20 ڈگری سینٹی گریڈ رہے گا، جبکہ کم سے کم درجہ حرارت {} ڈگری سینٹی گریڈ رہے گا۔"
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں صبح کا درجہ حرارت {morn_temp} ڈگری سینٹی گریڈ ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں صبح کا درجہ حرارت {morn_temp} ڈگری سینٹی گریڈ رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("morn_temp", morn_temp)]

class ActionHelloWorld(Action):
    
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_hello_world is called")

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionNightTemp(Action):
    
    def name(self) -> Text:
        return "action_utter_night_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_night_temp is called")
        
        # getting entity value of `city` and `day`
        received_city = next(tracker.get_latest_entity_values("city"), "لاہور")
        received_day = next(tracker.get_latest_entity_values("day"), "آج")
        
        print(received_city)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day)
        print(day_no_for_DB)
        
        # Getting most matched city name with custom function
        most_matched_city = get_matched_name(received_city, "city")[0]
        
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
        morn_temp = whole_JSON['daily'][0]['temp']['night']
        
        morn_temp = round(float(morn_temp) - 273.15, 2)
        
        # bot_response_to_send = "{} میں زیادہ سے زیادہ درجہ حرارت 20 ڈگری سینٹی گریڈ رہے گا، جبکہ کم سے کم درجہ حرارت {} ڈگری سینٹی گریڈ رہے گا۔"
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں رات کا درجہ حرارت {morn_temp} ڈگری سینٹی گریڈ ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں رات میں درجہ حرارت {morn_temp} ڈگری سینٹی گریڈ رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("morn_temp", morn_temp)]
