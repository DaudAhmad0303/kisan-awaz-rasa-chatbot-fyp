"""
Unofficial python wrapper for the Open Weather Map API.
"""

from datetime import datetime
import requests
# import heyoo


class Weather(object):
    """
    Weather Object
    """

    def __init__(self, apikey = None, lat = 31.577572, lng = 74.357416, duration = ['daily']):
        """
        Initialize the Weather Object

        Args:
            apikey[str]: API Key get from Open weather map API
            lat[float]: Latitude value of the area for which we want to know weather condition
            lng[float]: Longitude value of the area for which we want to know weather condition
            duration[list]: A list of durations for which we want to know the weather condition
                            i.e., 'hourly', 'minutely', 'current', 'daily', 'alerts'
                            
                            These should be as a list elements.
        """
        self.apikey = apikey
        self.lat = lat
        self.lng = lng
        exclude_list = ['hourly', 'minutely', 'current', 'daily', 'alerts']
        # We are removing all those elements which are provided by user as the results 
        # for these elements will be shown from api call which will not be present in api call
        # idea is to exclude all those words.
        for part in duration:
            if part in exclude_list:
                exclude_list.remove(part)
        self.exclude = ','.join(exclude_list)
        self.url = f"https://api.openweathermap.org/data/2.5/onecall?lat={self.lat}&lon={self.lng}&exclude={self.exclude}&appid={self.apikey}&units=metric"
    
    def send_api_call(self, ):
        '''Send an API call to `Open Weather Map` API and return a json response.'''
        r = requests.post(self.url)
        return r.json()

    def preprocess(self, data: str):
        """
        Preprocesses the data received from the API Call.

        This method is designed to only be used internally.

        Args:
            data[dict]: The data received from the API call `obj.send_api_call()`
        """
        if 'daily' in data:
            return data['daily']

    def get_forcast_time(self, data: str, day = 0):
        """
        Extracts the API call time when the response is received. 

        Args:
            data[dict]: The data received from the API call.
            day[int]:   The next day number for which you want to get the info.
        Returns:
            str: Time object received from `datetime.fromtimestamp`

        Example:
            >>> from openweathermap import Weather
            >>> weather = Weather(apikey, lat, lng)
            >>> time = weather.get_forcast_time(data = data, day = 1)
        """
        data = self.preprocess(data)
        if "dt" in data[day]:
            forcast_time = data[day]["dt"]
            return datetime.fromtimestamp(forcast_time)
    
    def get_min_max_temp(self, data: str, day = 0):
        """
        Extracts the `minimum` & `maximum` temperature from the provided data received from API call.

        Args:
            data[dict]: The data received from the API call.
            day[int]:   The next day number for which you want to get the info.
        Returns:
            tuple: minimum temperature and maximum temperature

        Example:
            >>> from openweathermap import Weather
            >>> weather = Weather(apikey, lat, lng)
            >>> min_temp, max_temp = weather.get_min_max_temp(data = data, day = 1)
        """
        data = self.preprocess(data)
        if "temp" in data[day]:
            min = data[day]["temp"]["min"]
            max = data[day]["temp"]["min"]
            return (min, max)
    
    def get_min_max_temp(self, data: str, day = 0):
        """
        Extracts the `minimum` & `maximum` temperature from the provided data received from API call.

        Args:
            data[dict]: The data received from the API call.
            day[int]:   The next day number for which you want to get the info.
        Returns:
            tuple: minimum temperature and maximum temperature

        Example:
            >>> from openweathermap import Weather
            >>> weather = Weather(apikey, lat, lng)
            >>> min_temp, max_temp = weather.get_min_max_temp(data = data, day = 1)
        """
        data = self.preprocess(data)
        if "temp" in data[day]:
            min = data[day]["temp"]["min"]
            max = data[day]["temp"]["min"]
            return (min, max)
    