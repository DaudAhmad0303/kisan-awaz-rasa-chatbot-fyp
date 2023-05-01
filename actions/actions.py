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
def get_weather_description(id: int) -> str:
    """Generates relative weather description based upon id from OpenWeatherMapAPI in Urdu.

    Args:
        id (int): ID of the Weather present in OpenWeatherMapAPI

    Returns:
        str: Description of the weather in Urdu relative to the ID.
    """
    weather_description = dict()
    weather_description = {
        # Thunderstorm Group
        200: "گرج چمک کے ساتھ ہلکی بارش",           # Thunderstorm with light rain
        201: "گرج چمک کے ساتھ بارش",                # Thunderstorm with rain
        202: "گرج چمک کے ساتھ تیز بارش",            # Thunderstorm with heavy rain
        210: "ہلکی گرج چمک",                        # Light Thunderstorm
        211: "گرج چمک",                             # Thunderstorm
        212: "شدید گرج چمک",                        # Heavy Thunderstorm
        221: "شدید گرج چمک والی طوفانی بارش",              # Ragged Thunderstorm
        230: "گرج چمک کے ساتھ ہلکی بوندا باندی",    # Thunderstorm with light drizzle
        231: "گرج چمک کے ساتھ بوندا باندی",         # Thunderstorn with drizzle
        232: "گرج چمک کے ساتھ تیز بوندا باندی",     # Thunderstorm with heavy drizzle
        
        # Drizzle Group
        300: "ہلکی ہلکی بوندا باندی",               # Light intensity drizzle
        301: "بوندا باندی",                         # Drizzle
        302: "موسلادھار بوندا باندی",                # Heavy intensity drizzle
        310: "ہلکی شدت کی بوندا باندی",             # Light intensity drizzle rain
        311: "بوندا باندی",                         # Drizzle rain
        312: "موسلادھار بوندا باندی",                # Heavy intensity drizzle rain
        313: "بارش اور بوندا باندی",                # Shower rain and drizzle
        314: "موسلادھار بارش اور بوندا باندی",       # Heavy shower rain and drizzle
        321: "بوندا باندی کی بوچھاڑ",               # Shower drizzle
        
        # Rain Group
        500: "بہت ہلکی بوندا باندی",             # Light Rain
        501: "ہلکی بارش",                        # Moderate Rain
        502: "شدید بارش",                        # Heavy intensity rain
        503: "بہت تیز بارش",                     # Very Heavy Rain
        504: "بہت شدید بارش",                    # Extreme Rain
        511: "برفیلی بارش",                      # Freezing Rain
        520: "ہلکی شدت کی بارش",                 # Light intensity Shower
        521: "بوندا باندی",                      # Shower Rain
        522: "موسلا دھار بارش",                   # Heavy intensity Shower Rain
        531: "سیلابی بارش",                       # Ragged Shower Rain
        
        # Snow Group
        600: "ہلکی برف باری",                   # Light snow
        601: "برفباری",                         # Snow
        602: "شدید برفباری",                    # Heavy snow
        611: "ژالہ باری",                       # Sleet
        612: "ہلکی بوچھاڑ والی ژالہ باری",      # Light shower sleet
        613: "بوچھاڑ والی ژالہ باری",           # shower sleet
        615: "ہلکی بارش کے ساتھ برفباری",       # light rain and snow
        616: "بارش اور برفباری",                # rain and snow
        620: "ہلکی بوچھاڑ والی برفباری",        # light shower snow
        621: "بوچھاڑ والی برفباری",             # shower snow
        622: "شدید بوچھاڑ والی برفباری",        # Heavy shower snow
        
        # Atmosphere Group
        701: "فضا میں ہلکی دھند چھائی",         # Mist
        711: "فضا میں دھواں دھواں پھیلا",             # Smoke
        721: "فضا میں گرد و غبار پھیلا",         # Haze
        731: "فضا میں ریت کے بگولہ چل رہے",     # Sand/Dust whirls
        741: "فضا میں دھند چھائی",              # Fog
        751: "فضا میں ریت اڑ رہی",              # Sand
        761: "فضا میں دھول کا سماں",            # Dust
        762: "فضا میں آتش فشاں راکھ اڑ رہی",        # Volcanic ash
        771: "تیز ہواوں کے طوفان چل رہے",       # Squalls
        781: "تیز آندھی چل رہی",                # Tornado
        
        # Clouds Group
        800: "آسمان صاف",                        # Clear Sky
        801: "آسمان پر تھوڑے بادل چھائے",        # Few Clouds
        802: "آسمان پر بکھرے بادل چھائے",        # Scattered Clouds
        803: "آسمان پر ٹوٹے بادل چھائے",         # Broken Clouds
        804: "آسمان پر ابر آلود بادل چھائے",     # Overcast Clouds
    }
    
    if id in weather_description:
        return weather_description[id] 
    else:
        return " "

"""class ActionSetGeoLocation(Action):
    
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
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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

class ActionHumidity(Action):
    
    def name(self) -> Text:
        return "action_utter_humidity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_humidity is called")
        
        # getting entity value of `city` and `day`
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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
        humidity = whole_JSON['daily'][day_no_for_DB]['humidity']
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں ہوا میں نمی کا تناسب {humidity} فیصد ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} کو {most_matched_city} میں ہوا میں نمی کا تناسب {humidity} فیصد رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("humidity", humidity)]

class ActionAirPressure(Action):
    
    def name(self) -> Text:
        return "action_utter_air_pressure"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_air_pressure is called")
        
        # getting entity value of `city` and `day`
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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
        air_pressure = whole_JSON['daily'][day_no_for_DB]['pressure']
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں ہوا کے دباو کا تناسب {air_pressure} ایچ پی اے ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} کو {most_matched_city} میں ہوا کے دباو کا تناسب {air_pressure} ایچ پی اے رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("air_pressure", air_pressure)]

class ActionWindSpeed(Action):
    
    def name(self) -> Text:
        return "action_utter_wind_speed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_wind_speed is called")
        
        # getting entity value of `city` and `day`
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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
        wind_speed = whole_JSON['daily'][day_no_for_DB]['wind_speed']
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں ہوا {wind_speed} کلو میٹر فی گنٹہ کی رفتار سے چل رہی ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} کو {most_matched_city} میں ہوا {wind_speed} کلو میٹر فی گنٹہ کی رفتار سے چل رہی ہوگی۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("wind_speed", wind_speed)]

class ActionUVindex(Action):
    
    def name(self) -> Text:
        return "action_utter_uv_index"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_uv_index is called")
        
        # getting entity value of `city` and `day`
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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
        uv_index = whole_JSON['daily'][day_no_for_DB]['uvi']
        
        if day_no_for_DB == 0:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں الٹرا وایلیٹ شعاعوں کا انڈیکس {uv_index} ہے۔"
        else:
            bot_response_to_send = f"{most_matched_day} کو {most_matched_city} میں الٹرا وایلیٹ شعاعوں کا انڈیکس {uv_index} رہے گا۔"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("uv_index", uv_index)]

class ActionWeather(Action):
    
    def name(self) -> Text:
        return "action_utter_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_utter_weather is called")
        
        # getting entity value of `city` and `day`
        received_city = tracker.get_slot("city")
        received_day = tracker.get_slot("day")
        
        print(received_city)
        print(received_day)
        
        # Getting most matched day name with custom function
        most_matched_day = get_matched_name(received_day, "day")[0]
        
        # Getting relative day-number for reteriving data from Database
        day_no_for_DB = relative_day_no(received_day, DB_update_time = time_DB_updated(formated=False))
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
        weather_id = whole_JSON['daily'][day_no_for_DB]['weather'][0]['id']
        
        urdu_weather_description = get_weather_description(weather_id)
        
        if day_no_for_DB == 0 or most_matched_day == "آج":
            if weather_id in range(200, 700):
                urdu_weather_description = f"{urdu_weather_description} ہو رہی ہے۔"
            elif weather_id in [701, 741]:
                urdu_weather_description = f"{urdu_weather_description} ہوئی ہے۔"
            elif weather_id in [711, 721]:
                urdu_weather_description = f"{urdu_weather_description} ہوا ہے۔"
            elif weather_id in [731, 771]:
                urdu_weather_description = f"{urdu_weather_description} ہیں۔"
            elif weather_id in [751, 761, 762, 781, 800]:
                urdu_weather_description = f"{urdu_weather_description} ہے۔"
            elif weather_id in [801, 802, 803, 804]:
                urdu_weather_description = f"{urdu_weather_description} ہوئے ہیں۔"
        else:
            if weather_id in range(200, 700):
                urdu_weather_description = f"{urdu_weather_description} ہو رہی ہوگی۔"
            elif weather_id in [701, 741]:
                urdu_weather_description = f"{urdu_weather_description} ہوئی ہوگی۔"
            elif weather_id in [711, 721]:
                urdu_weather_description = f"{urdu_weather_description} ہوا گا۔"
            elif weather_id in [731, 771, 801, 802, 803, 804]:
                urdu_weather_description = f"{urdu_weather_description} ہوں گے۔"
            elif weather_id in [761, 800]:
                urdu_weather_description = f"{urdu_weather_description} ہوگا۔"
            elif weather_id in [751, 762, 781, 800]:
                urdu_weather_description = f"{urdu_weather_description} ہوگی۔"
        
        
        if day_no_for_DB == 0 or most_matched_day == "آج":
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں {urdu_weather_description}"
        else:
            bot_response_to_send = f"{most_matched_day} {most_matched_city} میں {urdu_weather_description}"
        
        dispatcher.utter_message(text=bot_response_to_send)

        return [SlotSet("weather_id", weather_id)]

