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
from pprint import pprint


client = mongo.MongoClient("mongodb://localhost:27017")
print(client)

db1 = client["KisanAwaz"]       # City Geolocations DB
db2 = client["weatherData"]     # API Fetched Weather Data DB

geoLocationsCollection = db1["CityGeoLocations"]

allDatabases = client.list_database_names()
pprint(allDatabases)
allCollectionsInWeatherDB = list(db2.list_collections())
# pprint(allCollectionsInWeatherDB, len(len(allCollectionsInWeatherDB)))


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_hello_world is called")

        dispatcher.utter_message(text="Hello World!")

        return []

# class ActionSetGeoLocation(Action):
    
#     def name(self) -> Text:
#         return "action_set_geo_location"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         received_city = next(tracker.get_slot("city"), None)
#         document = collection1.find_one({'city': received_city})
#         print(document)
#         latitude = float(document['latitude'])
#         longitude = float(document['longitude'])
        
        
#         # dispatcher.utter_message(text="Hello World!")

#         return []



class ActionMornTemp(Action):
    
    def name(self) -> Text:
        return "action_utter_morn_temp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # getting entity value of `city` and `day`
        print("action_utter_morn_temp is called")
        received_city = next(tracker.get_latest_entity_values("city"), None)
        received_day = next(tracker.get_latest_entity_values("day"), None)
        
        print(received_city)
        document = geoLocationsCollection.find_one({'city': received_city})
        print(document)
        
        most_matched_city = received_city
        day = 0
        latitude = float(document['latitude'])
        longitude = float(document['longitude'])
        
        collection2 = db2[received_city]
        
        whole_JSON = collection2.find(
            {
                "lat": latitude,
                "lon": longitude,
            }
        )
        day_temp = whole_JSON['daily'][0]['temp']['day']
        
        # bot_response_to_send = "{} میں زیادہ سے زیادہ درجہ حرارت 20 ڈگری سینٹی گریڈ رہے گا، جبکہ کم سے کم درجہ حرارت {} ڈگری سینٹی گریڈ رہے گا۔"
        if day == 0:
            bot_response_to_send = f"{received_day} {most_matched_city} میں صبح کا درجہ حرارت {day_temp} ڈگری سینٹی گریڈ ہے۔"
        else:
            bot_response_to_send = f"{received_day} {most_matched_city} میں صبح کا درجہ حرارت {day_temp} ڈگری سینٹی گریڈ رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("morn_temp", day_temp)]
