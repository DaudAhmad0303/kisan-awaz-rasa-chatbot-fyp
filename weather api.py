from datetime import datetime
import requests
API_key = "5af4c2482556ed487ddf572a2f3088c8"
# r = requests.post(f"https://api.openweathermap.org/data/2.5/onecall?lat=31.577572&lon=74.357416&exclude=hourly,minutely,current&appid={API_key}")
# print(r.json())
response1 = {
    'lat': 31.5776,
    'lon': 74.3574,
    'timezone': 'Asia/Karachi',
    'timezone_offset': 18000,
    'current': {
        'dt': 1659536758,
        'sunrise': 1659485980,
        'sunset': 1659535069,
        'temp': 304.14,
        'feels_like': 308.48,
        'pressure': 1000,
        'humidity': 62,
        'dew_point': 296,
        'uvi': 0,
        'clouds': 40,
        'visibility': 5000,
        'wind_speed': 2.57,
        'wind_deg': 330,
        'weather':
            [
                {
                    'id': 711,
                    'main': 'Smoke',
                    'description': 'smoke',
                    'icon': '50n'
                }
            ]
        },
    'minutely': [
        {
            'dt': 1659536760,
            'precipitation': 0
            },
        {
            'dt': 1659536820,
            'precipitation': 0
            },
        {
            'dt': 1659536880,
            'precipitation': 0
            },
        {
            'dt': 1659536940,
            'precipitation': 0
            },
        {
            'dt': 1659537000,
            'precipitation': 0
            },
        {
            'dt': 1659537060,
            'precipitation': 0
            },
        {
            'dt': 1659537120,
            'precipitation': 0
            },
        {
            'dt': 1659537180,
            'precipitation': 0
            },
        {
            'dt': 1659537240,
            'precipitation': 0
            },
        {
            'dt': 1659537300,
            'precipitation': 0
            },
        {
            'dt': 1659537360,
            'precipitation': 0
            },
        {
            'dt': 1659537420,
            'precipitation': 0
            },
        {
            'dt': 1659537480,
            'precipitation': 0
            },
        {
            'dt': 1659537540,
            'precipitation': 0
            },
        {
            'dt': 1659537600,
            'precipitation': 0
            },
        {
            'dt': 1659537660,
            'precipitation': 0
            },
        {
            'dt': 1659537720,
            'precipitation': 0
            },
        {
            'dt': 1659537780,
            'precipitation': 0
            },
        {
            'dt': 1659537840,
            'precipitation': 0
            },
        {
            'dt': 1659537900,
            'precipitation': 0
            },
        {
            'dt': 1659537960,
            'precipitation': 0
            },
        {
            'dt': 1659538020,
            'precipitation': 0
            },
        {
            'dt': 1659538080,
            'precipitation': 0
            },
        {
            'dt': 1659538140,
            'precipitation': 0
            },
        {
            'dt': 1659538200,
            'precipitation': 0
            },
        {
            'dt': 1659538260,
            'precipitation': 0
            },
        {
            'dt': 1659538320,
            'precipitation': 0
            },
        {
            'dt': 1659538380,
            'precipitation': 0
            },
        {
            'dt': 1659538440,
            'precipitation': 0
            },
        {
            'dt': 1659538500,
            'precipitation': 0
            },
        {
            'dt': 1659538560,
            'precipitation': 0
            },
        {
            'dt': 1659538620,
            'precipitation': 0
            },
        {
            'dt': 1659538680,
            'precipitation': 0
            },
        {
            'dt': 1659538740,
            'precipitation': 0
            },
        {
            'dt': 1659538800,
            'precipitation': 0
            },
        {
            'dt': 1659538860,
            'precipitation': 0
            },
        {
            'dt': 1659538920,
            'precipitation': 0
            },
        {
            'dt': 1659538980,
            'precipitation': 0
            },
        {
            'dt': 1659539040,
            'precipitation': 0
            }, 
        {
            'dt': 1659539100,
            'precipitation': 0
            },
        {
            'dt': 1659539160,
            'precipitation': 0
            },
        {
            'dt': 1659539220,
            'precipitation': 0
            },
        {
            'dt': 1659539280,
            'precipitation': 0
            },
        {
            'dt': 1659539340,
            'precipitation': 0
            },
        {
            'dt': 1659539400,
            'precipitation': 0
            },
        {
            'dt': 1659539460,
            'precipitation': 0
            },
        {
            'dt': 1659539520,
            'precipitation': 0
            },
        {
            'dt': 1659539580,
            'precipitation': 0
            },
        {
            'dt': 1659539640,
            'precipitation': 0
            },
        {
            'dt': 1659539700,
            'precipitation': 0
            },
        {
            'dt': 1659539760,
            'precipitation': 0
            },
        {
            'dt': 1659539820,
            'precipitation': 0
            },
        {
            'dt': 1659539880,
            'precipitation': 0
            },
        {
            'dt': 1659539940,
            'precipitation': 0
            },
        {
            'dt': 1659540000,
            'precipitation': 0
            },
        {
            'dt': 1659540060,
            'precipitation': 0
            },
        {
            'dt': 1659540120,
            'precipitation': 0
            },
        {
            'dt': 1659540180,
            'precipitation': 0
            },
        {
            'dt': 1659540240,
            'precipitation': 0
            },
        {
            'dt': 1659540300,
            'precipitation': 0
            },
        {
            'dt': 1659540360,
            'precipitation': 0
            }
        ]
    }

response2 = {
    "lat": 31.5776,
    "lon": 74.3574,
    "timezone": "Asia/Karachi",
    "timezone_offset": 18000,
    "daily": [
        {
            "dt": 1659510000,
            "sunrise": 1659485980,
            "sunset": 1659535069,
            "moonrise": 1659503760,
            "moonset": 1659546960,
            "moon_phase": 0.18,
            "temp": {
                "day": 310.53,
                "min": 303.41,
                "max": 311.23,
                "night": 304.6,
                "eve": 305.82,
                "morn": 303.86
            },
            "feels_like": {
                "day": 316.05,
                "night": 309.53,
                "eve": 310.85,
                "morn": 309.42
            },
            "pressure": 1001,
            "humidity": 42,
            "dew_point": 295.8,
            "wind_speed": 3.04,
            "wind_deg": 195,
            "wind_gust": 4.94,
            "weather": [
                {
                    "id": 501,
                    "main": "Rain",
                    "description": "moderate rain",
                    "icon": "10d"
                }
            ],
            "clouds": 8,
            "pop": 0.73,
            "rain": 1.36,
            "uvi": 8.49
        },
        {
            "dt": 1659596400,
            "sunrise": 1659572420,
            "sunset": 1659621420,
            "moonrise": 1659593760,
            "moonset": 1659635160,
            "moon_phase": 0.21,
            "temp": {
                "day": 309.85,
                "min": 302.45,
                "max": 310.63,
                "night": 303.28,
                "eve": 303.43,
                "morn": 302.52
            },
            "feels_like": {
                "day": 316.23,
                "night": 306.65,
                "eve": 309.14,
                "morn": 307.56
            },
            "pressure": 1001,
            "humidity": 46,
            "dew_point": 296.68,
            "wind_speed": 4.79,
            "wind_deg": 163,
            "wind_gust": 8.21,
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10d"
                }
            ],
            "clouds": 1,
            "pop": 0.4,
            "rain": 2.56,
            "uvi": 10.78
        },
        {
            "dt": 1659682800,
            "sunrise": 1659658859,
            "sunset": 1659707771,
            "moonrise": 1659683940,
            "moonset": 1659723660,
            "moon_phase": 0.25,
            "temp": {
                "day": 306.66,
                "min": 301.17,
                "max": 307.81,
                "night": 302.13,
                "eve": 305.94,
                "morn": 301.17
            },
            "feels_like": {
                "day": 312.86,
                "night": 307.62,
                "eve": 312.84,
                "morn": 305.3
            },
            "pressure": 1001,
            "humidity": 57,
            "dew_point": 297.03,
            "wind_speed": 3.41,
            "wind_deg": 129,
            "wind_gust": 6.78,
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10d"
                }
            ],
            "clouds": 94,
            "pop": 0.67,
            "rain": 2.12,
            "uvi": 10.87
        },
        {
            "dt": 1659769200,
            "sunrise": 1659745299,
            "sunset": 1659794121,
            "moonrise": 1659774360,
            "moonset": 0,
            "moon_phase": 0.28,
            "temp": {
                "day": 307.47,
                "min": 300.64,
                "max": 309.76,
                "night": 304.93,
                "eve": 309.08,
                "morn": 300.72
            },
            "feels_like": {
                "day": 313.74,
                "night": 310.61,
                "eve": 315.24,
                "morn": 304.33
            },
            "pressure": 999,
            "humidity": 54,
            "dew_point": 296.93,
            "wind_speed": 3.04,
            "wind_deg": 144,
            "wind_gust": 5.66,
            "weather": [
                {
                    "id": 802,
                    "main": "Clouds",
                    "description": "scattered clouds",
                    "icon": "03d"
                }
            ],
            "clouds": 27,
            "pop": 0.33,
            "uvi": 11.11
        },
        {
            "dt": 1659855600,
            "sunrise": 1659831739,
            "sunset": 1659880469,
            "moonrise": 1659864900,
            "moonset": 1659812460,
            "moon_phase": 0.32,
            "temp": {
                "day": 308.83,
                "min": 301.47,
                "max": 311.4,
                "night": 301.47,
                "eve": 304.57,
                "morn": 303.77
            },
            "feels_like": {
                "day": 314.23,
                "night": 306.42,
                "eve": 310.94,
                "morn": 309.75
            },
            "pressure": 996,
            "humidity": 47,
            "dew_point": 295.98,
            "wind_speed": 6.03,
            "wind_deg": 133,
            "wind_gust": 11.68,
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10d"
                }
            ],
            "clouds": 86,
            "pop": 0.67,
            "rain": 4.16,
            "uvi": 11.41
        },
        {
            "dt": 1659942000,
            "sunrise": 1659918178,
            "sunset": 1659966816,
            "moonrise": 1659955500,
            "moonset": 1659901680,
            "moon_phase": 0.35,
            "temp": {
                "day": 303.27,
                "min": 299.91,
                "max": 304.74,
                "night": 301.23,
                "eve": 304.4,
                "morn": 299.91
            },
            "feels_like": {
                "day": 308.99,
                "night": 305.77,
                "eve": 310.5,
                "morn": 303.21
            },
            "pressure": 1000,
            "humidity": 72,
            "dew_point": 297.76,
            "wind_speed": 4.94,
            "wind_deg": 123,
            "wind_gust": 9.97,
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10d"
                }
            ],
            "clouds": 98,
            "pop": 0.73,
            "rain": 4.56,
            "uvi": 12
        },
        {
            "dt": 1660028400,
            "sunrise": 1660004618,
            "sunset": 1660053162,
            "moonrise": 1660045920,
            "moonset": 1659991560,
            "moon_phase": 0.39,
            "temp": {
                "day": 307.16,
                "min": 300.79,
                "max": 309.42,
                "night": 303.96,
                "eve": 309.16,
                "morn": 300.79
            },
            "feels_like": {
                "day": 313.74,
                "night": 309.96,
                "eve": 315.87,
                "morn": 304.77
            },
            "pressure": 998,
            "humidity": 56,
            "dew_point": 297.14,
            "wind_speed": 2.92,
            "wind_deg": 150,
            "wind_gust": 4.62,
            "weather": [
                {
                    "id": 804,
                    "main": "Clouds",
                    "description": "overcast clouds",
                    "icon": "04d"
                }
            ],
            "clouds": 97,
            "pop": 0.18,
            "uvi": 12
        },
        {
            "dt": 1660114800,
            "sunrise": 1660091058,
            "sunset": 1660139507,
            "moonrise": 1660135980,
            "moonset": 1660081920,
            "moon_phase": 0.43,
            "temp": {
                "day": 308.77,
                "min": 302.2,
                "max": 311.02,
                "night": 304.54,
                "eve": 309.25,
                "morn": 302.2
            },
            "feels_like": {
                "day": 315.76,
                "night": 310.26,
                "eve": 316.25,
                "morn": 306.97
            },
            "pressure": 995,
            "humidity": 51,
            "dew_point": 297.34,
            "wind_speed": 5.26,
            "wind_deg": 128,
            "wind_gust": 11.52,
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "clouds": 0,
            "pop": 0.16,
            "uvi": 12
        }
    ]
}

response3 = {
    "lat": 31.5776,
    "lon": 74.3574,
    "timezone": "Asia/Karachi",
    "timezone_offset": 18000,
    "daily": [
        {
            "dt": 1662962400,
            "sunrise": 1662943482,
            "sunset": 1662988416,
            "moonrise": 1662993360,
            "moonset": 1662949740,
            "moon_phase": 0.57,
            "temp": {
                "day": 33.16,
                "min": 25.22,
                "max": 35.3,
                "night": 29.99,
                "eve": 33.87,
                "morn": 25.37
            },
            "feels_like": {
                "day": 36.32,
                "night": 33.22,
                "eve": 36.56,
                "morn": 25.95
            },
            "pressure": 1004,
            "humidity": 49,
            "dew_point": 21.11,
            "wind_speed": 3.12,
            "wind_deg": 27,
            "wind_gust": 5.16,
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "clouds": 0,
            "pop": 0.25,
            "uvi": 5.87
        },
        {
            "dt": 1663048800,
            "sunrise": 1663029917,
            "sunset": 1663074737,
            "moonrise": 1663081560,
            "moonset": 1663039860,
            "moon_phase": 0.6,
            "temp": {
                "day": 33.52,
                "min": 25.61,
                "max": 35.51,
                "night": 28.29,
                "eve": 34.1,
                "morn": 25.76
            },
            "feels_like": {
                "day": 36.46,
                "night": 30.53,
                "eve": 37.31,
                "morn": 26.17
            },
            "pressure": 1005,
            "humidity": 47,
            "dew_point": 20.72,
            "wind_speed": 3.04,
            "wind_deg": 56,
            "wind_gust": 4.73,
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "clouds": 0,
            "pop": 0,
            "uvi": 8.91
        },
        {
            "dt": 1663135200,
            "sunrise": 1663116352,
            "sunset": 1663161059,
            "moonrise": 1663169820,
            "moonset": 1663129980,
            "moon_phase": 0.64,
            "temp": {
                "day": 34.35,
                "min": 26.22,
                "max": 36.07,
                "night": 28.36,
                "eve": 34.08,
                "morn": 26.51
            },
            "feels_like": {
                "day": 37.82,
                "night": 30.66,
                "eve": 37.27,
                "morn": 26.51
            },
            "pressure": 1006,
            "humidity": 46,
            "dew_point": 21.26,
            "wind_speed": 3.87,
            "wind_deg": 15,
            "wind_gust": 5.73,
            "weather": [
                {
                    "id": 801,
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d"
                }
            ],
            "clouds": 13,
            "pop": 0.09,
            "uvi": 8.79
        },
        {
            "dt": 1663221600,
            "sunrise": 1663202787,
            "sunset": 1663247380,
            "moonrise": 1663258320,
            "moonset": 1663219980,
            "moon_phase": 0.67,
            "temp": {
                "day": 33.15,
                "min": 25.94,
                "max": 35.53,
                "night": 28.32,
                "eve": 33.77,
                "morn": 26.13
            },
            "feels_like": {
                "day": 36.59,
                "night": 30.72,
                "eve": 37.26,
                "morn": 26.13
            },
            "pressure": 1005,
            "humidity": 50,
            "dew_point": 21.47,
            "wind_speed": 3.39,
            "wind_deg": 85,
            "wind_gust": 6.32,
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "clouds": 0,
            "pop": 0.09,
            "uvi": 8.6
        },
        {
            "dt": 1663308000,
            "sunrise": 1663289221,
            "sunset": 1663333700,
            "moonrise": 1663347060,
            "moonset": 1663309980,
            "moon_phase": 0.7,
            "temp": {
                "day": 34.22,
                "min": 26.54,
                "max": 35.79,
                "night": 28.91,
                "eve": 33,
                "morn": 26.54
            },
            "feels_like": {
                "day": 37.55,
                "night": 31.19,
                "eve": 36.29,
                "morn": 26.54
            },
            "pressure": 1001,
            "humidity": 46,
            "dew_point": 20.97,
            "wind_speed": 3.18,
            "wind_deg": 106,
            "wind_gust": 5.43,
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10d"
                }
            ],
            "clouds": 0,
            "pop": 0.38,
            "rain": 0.25,
            "uvi": 8.64
        },
        {
            "dt": 1663394400,
            "sunrise": 1663375656,
            "sunset": 1663420021,
            "moonrise": 1663435980,
            "moonset": 1663399860,
            "moon_phase": 0.73,
            "temp": {
                "day": 33.02,
                "min": 21.91,
                "max": 34.69,
                "night": 22.93,
                "eve": 31.35,
                "morn": 25.56
            },
            "feels_like": {
                "day": 36.62,
                "night": 23.5,
                "eve": 34.33,
                "morn": 26.13
            },
            "pressure": 1002,
            "humidity": 51,
            "dew_point": 21.52,
            "wind_speed": 5.05,
            "wind_deg": 120,
            "wind_gust": 7.13,
            "weather": [
                {
                    "id": 501,
                    "main": "Rain",
                    "description": "moderate rain",
                    "icon": "10d"
                }
            ],
            "clouds": 0,
            "pop": 0.95,
            "rain": 5.28,
            "uvi": 9
        },
        {
            "dt": 1663480800,
            "sunrise": 1663462091,
            "sunset": 1663506342,
            "moonrise": 1663525320,
            "moonset": 1663489620,
            "moon_phase": 0.75,
            "temp": {
                "day": 29.6,
                "min": 21.94,
                "max": 30.5,
                "night": 22.62,
                "eve": 26.45,
                "morn": 21.94
            },
            "feels_like": {
                "day": 31.23,
                "night": 23.08,
                "eve": 26.45,
                "morn": 22.51
            },
            "pressure": 1005,
            "humidity": 55,
            "dew_point": 19.8,
            "wind_speed": 5.2,
            "wind_deg": 106,
            "wind_gust": 8.11,
            "weather": [
                {
                    "id": 803,
                    "main": "Clouds",
                    "description": "broken clouds",
                    "icon": "04d"
                }
            ],
            "clouds": 79,
            "pop": 0,
            "uvi": 9
        },
        {
            "dt": 1663567200,
            "sunrise": 1663548527,
            "sunset": 1663592662,
            "moonrise": 0,
            "moonset": 1663579080,
            "moon_phase": 0.79,
            "temp": {
                "day": 23.6,
                "min": 22.46,
                "max": 24.89,
                "night": 23.2,
                "eve": 24.89,
                "morn": 23.04
            },
            "feels_like": {
                "day": 24.16,
                "night": 23.95,
                "eve": 25.5,
                "morn": 23.54
            },
            "pressure": 1007,
            "humidity": 82,
            "dew_point": 20.35,
            "wind_speed": 5.23,
            "wind_deg": 60,
            "wind_gust": 7.39,
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10d"
                }
            ],
            "clouds": 90,
            "pop": 0.53,
            "rain": 2.48,
            "uvi": 9
        }
    ]
}

print('First Day of Weather Forcast:', datetime.fromtimestamp(1662962400))
print('Last Day of Weather Forcast: ', datetime.fromtimestamp(1663567200))