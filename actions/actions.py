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
from openweathermap.APIToMongoDB import time_DB_updated

client = mongo.MongoClient("mongodb://localhost:27017")
print(client)

db = client["KisanAwaz"]       # City Geolocations DB
# db2 = client["weatherData"]     # API Fetched Weather Data DB

geo_locations_collection = db["CityGeoLocations"]

weather_forecast_collection = db["WeatherForecast"]

print("Database updated on", time_DB_updated())

# allDatabases = client.list_database_names()
# pprint(allDatabases)

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
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day)
        print(day_no_for_DB)
        
        # Getting most matched city name with custom function
        most_matched_city = get_matched_name(name = received_city, name_type="city")[0]
        
        # Getting the GeoLocations' Document of `city` from Database
        document = geo_locations_collection.find_one({'city': most_matched_city})
        print(document)
        
        latitude = float(document['latitude'])
        longitude = float(document['longitude'])
        
        # Getting Whole JSON/Document from DB of desired city
        whole_JSON = weather_forecast_collection.find_one(
            {
                "lat": latitude,
                "lon": longitude
            }
        )
        # print(whole_JSON, type(whole_JSON))
        
        # Getting desired weather service
        morn_temp = whole_JSON['daily'][day_no_for_DB]['temp']['morn']
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں صبح کا درجہ حرارت {morn_temp} ڈگری سینٹی گریڈ ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں صبح کا درجہ حرارت {morn_temp} ڈگری سینٹی گریڈ رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("morn_temp", morn_temp)]

class ActionEveTemp(Action):
    
    def name(self) -> Text:
        return "action_utter_eve_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_eve_temp is called")
        
        # getting entity value of `city` and `day`
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day)
        print(day_no_for_DB)
        
        # Getting most matched city name with custom function
        most_matched_city = get_matched_name(received_city, "city")[0]
        
        # Getting the GeoLocations' Document of `city` from Database
        document = geo_locations_collection.find_one({'city': most_matched_city})
        print(document)
        
        latitude = float(document['latitude'])
        longitude = float(document['longitude'])
        
        # Getting Whole JSON/Document from DB of desired city
        whole_JSON = weather_forecast_collection.find_one(
            {
                "lat": latitude,
                "lon": longitude
            }
        )
        # print(whole_JSON, type(whole_JSON))
        
        # Getting desired weather service
        eve_temp = whole_JSON['daily'][day_no_for_DB]['temp']['eve']
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں شام کا درجہ حرارت {eve_temp} ڈگری سینٹی گریڈ ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} کو {most_matched_city} میں شام کا درجہ حرارت {eve_temp} ڈگری سینٹی گریڈ رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("eve_temp", eve_temp)]

class ActionNightTemp(Action):
    
    def name(self) -> Text:
        return "action_utter_night_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_night_temp is called")
        
        # getting entity value of `city` and `day`
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day)
        print(day_no_for_DB)
        
        # Getting most matched city name with custom function
        most_matched_city = get_matched_name(received_city, "city")[0]
        
        # Getting the GeoLocations' Document of `city` from Database
        document = geo_locations_collection.find_one({'city': most_matched_city})
        print(document)
        
        latitude = float(document['latitude'])
        longitude = float(document['longitude'])
        
        # Getting Whole JSON/Document from DB of desired city
        whole_JSON = weather_forecast_collection.find_one(
            {
                "lat": latitude,
                "lon": longitude
            }
        )
        # print(whole_JSON, type(whole_JSON))
        
        # Getting desired weather service
        night_temp = whole_JSON['daily'][day_no_for_DB]['temp']['night']
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں رات کا درجہ حرارت {night_temp} ڈگری سینٹی گریڈ ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں رات میں درجہ حرارت {night_temp} ڈگری سینٹی گریڈ رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("night_temp", night_temp)]

class ActionMinTemp(Action):
    
    def name(self) -> Text:
        return "action_utter_min_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_min_temp is called")
        
        # getting entity value of `city` and `day`
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day)
        print(day_no_for_DB)
        
        # Getting most matched city name with custom function
        most_matched_city = get_matched_name(received_city, "city")[0]
        
        # Getting the GeoLocations' Document of `city` from Database
        document = geo_locations_collection.find_one({'city': most_matched_city})
        print(document)
        
        latitude = float(document['latitude'])
        longitude = float(document['longitude'])
        
        # Getting Whole JSON/Document from DB of desired city
        whole_JSON = weather_forecast_collection.find_one(
            {
                "lat": latitude,
                "lon": longitude
            }
        )
        # print(whole_JSON, type(whole_JSON))
        
        # Getting desired weather service
        min_temp = whole_JSON['daily'][day_no_for_DB]['temp']['min']
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں کم سے کم درجہ حرارت {min_temp} ڈگری سینٹی گریڈ ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} کو {most_matched_city} میں کم سے کم درجہ حرارت {min_temp} ڈگری سینٹی گریڈ رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("min_temp", min_temp)]

class ActionMaxTemp(Action):
    
    def name(self) -> Text:
        return "action_utter_max_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_max_temp is called")
        
        # getting entity value of `city` and `day`
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day)
        print(day_no_for_DB)
        
        # Getting most matched city name with custom function
        most_matched_city = get_matched_name(received_city, "city")[0]
        
        # Getting the GeoLocations' Document of `city` from Database
        document = geo_locations_collection.find_one({'city': most_matched_city})
        print(document)
        
        latitude = float(document['latitude'])
        longitude = float(document['longitude'])
        
        # Getting Whole JSON/Document from DB of desired city
        whole_JSON = weather_forecast_collection.find_one(
            {
                "lat": latitude,
                "lon": longitude
            }
        )
        # print(whole_JSON, type(whole_JSON))
        
        # Getting desired weather service
        max_temp = whole_JSON['daily'][day_no_for_DB]['temp']['max']
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں زیادہ سے زیادہ درجہ حرارت {max_temp} ڈگری سینٹی گریڈ ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} کو {most_matched_city} میں زیادہ سے زیادہ درجہ حرارت {max_temp} ڈگری سینٹی گریڈ رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("max_temp", max_temp)]

class ActionMinMaxTemp(Action):
    
    def name(self) -> Text:
        return "action_utter_min_max_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_min_max_temp is called")
        
        # getting entity value of `city` and `day`
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day)
        print(day_no_for_DB)
        
        # Getting most matched city name with custom function
        most_matched_city = get_matched_name(received_city, "city")[0]
        
        # Getting the GeoLocations' Document of `city` from Database
        document = geo_locations_collection.find_one({'city': most_matched_city})
        print(document)
        
        latitude = float(document['latitude'])
        longitude = float(document['longitude'])
        
        # Getting Whole JSON/Document from DB of desired city
        whole_JSON = weather_forecast_collection.find_one(
            {
                "lat": latitude,
                "lon": longitude
            }
        )
        # print(whole_JSON, type(whole_JSON))
        
        # Getting desired weather service
        min_temp = whole_JSON['daily'][day_no_for_DB]['temp']['min']
        max_temp = whole_JSON['daily'][day_no_for_DB]['temp']['max']
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں کم سے کم درجہ حرارت {min_temp} ڈگری سینٹی گریڈ ہے، جبکہ زیادہ سے زیادہ درجہ حرارت {max_temp} ڈگری سینٹی گریڈ ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} کو {most_matched_city} میں کم سے کم درجہ حرارت {min_temp} ڈگری سینٹی گریڈ رہے گا، جبکہ زیادہ سے زیادہ درجہ حرارت {max_temp} ڈگری سینٹی گریڈ رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("min_temp", min_temp), SlotSet("max_temp", max_temp)]
