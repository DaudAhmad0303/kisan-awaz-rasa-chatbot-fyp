# from openweathermap import Weather
latitude, longitude = 31.577572, 74.357416
# day = 2
# apikey = "5af4c2482556ed487ddf572a2f3088c8"
# weather = Weather(apikey= apikey, lat= latitude, lng= longitude)
# data = weather.send_api_call()
# time = weather.get_forcast_time(data, day=day)
# print(time)
# print(type(time), '\n---------------------')
# min_temp, max_temp = weather.get_min_max_temp(data, day= day)
# print(f"Maximum Temperature got on {time} is {min_temp} °C and minimum temperature got is {max_temp} °C at UET Lahore.\n\n\n\n")

# ---------------------------------------------------------------------------
# exclude_list = ['hourly', 'minutely', 'current', 'daily', 'alerts']
# duration = ['daily']
# for part in duration:
#     if part in exclude_list:
#         exclude_list.remove(part)
# print(exclude_list)

# -----------------------------------------------------------------------------
from pyowm import OWM
from pyowm.utils import timestamps
# from pyowm.utils import config
owm = OWM('5af4c2482556ed487ddf572a2f3088c8')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=latitude, lon=longitude)
# forecast = mgr.forecast_at_place('Milan,IT', 'daily')
# answer = forecast.will_be_clear_at(timestamps.tomorrow())
# print(timestamps.tomorrow())
# print(answer)
# print(one_call.forecast_daily[0].temperature('celsius'))
print(one_call.forecast_daily[0].wind())
# print(one_call.forecast_daily[0].temperature('celsius').get('feels_like_morn', None))